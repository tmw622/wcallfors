from django.db import models
import datetime as d
from sc.models import TSelectCourse
import pymysql

# Create your models here.

class Tstudent(models.Model):
    stuid=models.AutoField(primary_key=True)
    stuno=models.CharField(max_length=50)
    stuname=models.CharField(max_length=50)
    selectcourse=models.ForeignKey('sc.TSelectCourse',
                                   on_delete=models.CASCADE,db_column='scid')
    class Meta:
        db_table='Tstudent'

    def getrate(self):
        calldate=Tcalldate.objects.filter(selectcourse=self.selectcourse)
        calllist=[]
        rate="0%"
        attendlist=[]
        for row in calldate:
            calldateid=row.calldateid
            callrec=Tcallrec.objects.filter(calldate=row,student=self)
            attendrec=Tcallrec.objects.filter(calldate=row,student=self,iscall=1)

            if callrec.count()!=0:
                calllist.append(callrec[0])
            if attendrec.count()!=0:
                attendlist.append(attendrec[0])

        if calldate.count()!=0:
            totalcount=calldate.count()
            acount=len(attendlist)
            if totalcount!=0:
                acrate=acount/totalcount
                acrate='%.2f%%'%(acrate*100)
        return acrate

class Tcalldate(models.Model):
    calldateid=models.AutoField(primary_key=True)
    calldate=models.DateTimeField()
    selectcourse=models.ForeignKey('sc.TSelectCourse',
                                   on_delete=models.CASCADE,db_column='scid')
    class Meta:
        db_table='Tcalldate'

    def StartNewDate(scid):
        nowtime=d.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        calldate =Tcalldate()
        calldate.calldate=nowtime

        sc=TSelectCourse.objects.get(scid=scid)
        calldate.selectcourse=sc
        calldate.save()
        calldateid=calldate.calldateid
        return calldateid

    def getmaxid(scid):
        sql="select * from tcalldate where scid="+str(scid.scid)+" order by calldate desc limit 1"
        lastdate=Tcalldate.objects.raw(sql)
        calldateid=lastdate[0].calldateid
        return calldateid

class Tcallrec(models.Model):
    callrecid=models.AutoField(primary_key=True)
    iscall=models.BooleanField()
    calldate=models.ForeignKey('Tcalldate',on_delete=models.CASCADE,db_column='calldateid')
    student=models.ForeignKey('Tstudent',
                                   on_delete=models.CASCADE,db_column='stuid')
    calltime=models.DateTimeField(null=True)
    callip=models.CharField(max_length=45, null=True)

    class Meta:
        db_table='Tcallrec'

    def InitialSign(scid):
        calldateid=Tcalldate.StartNewDate(scid)

        db=pymysql.connect("localhost","root","python3020","wsign")
        cursor=db.cursor()

        sql="select s.stuid, c.calldateid from Tstudent s, Tcalldate c where  s.scid=c.scid and c.calldateid="+str(calldateid)+""
        cursor.execute(sql)
        data=cursor.fetchall()
        for row in data:
            sql="insert into tcallrec(calldateid,stuid,iscall)  value(%s,%s,%s)"
            values=(row[1],row[0],0)
            cursor.execute(sql,values)
            db.commit()
        cursor.close()
        db.close()
        calldate=Tcalldate.objects.get(calldateid=calldateid)
        calllist=Tcallrec.objects.filter(calldate=calldate)
        context={'calllist':calllist,'calldateid':calldateid}
        return context;

    def callhis(scid,calldateid):
        scid=TSelectCourse.objects.get(scid=scid)
        calldatelist=Tcalldate.objects.filter(selectcourse=scid)
        if calldateid == 0:
            calldateid=Tcalldate.getmaxid(scid)
            calldate=Tcalldate.objects.get(calldateid=calldateid)
            calllist=Tcallrec.objects.filter(calldate=calldate)
        else:
            calldate = Tcalldate.objects.get(calldateid=calldateid)
            calllist = Tcallrec.objects.filter(calldate=calldate)
        context={'calldatelist':calldatelist,'callreclist':calllist,'calldateid':calldateid}
        return context

    def statics(calldateid):
        calldate = Tcalldate.objects.get(calldateid=calldateid)
        totalstu = Tcallrec.objects.filter(calldate=calldate)
        attend = Tcallrec.objects.filter(calldate=calldate, iscall=1)
        if totalstu.count()==0:
            rate="0%"
        else:
            rate = attend.count() / totalstu.count()
            rate = '%.2f%%' %(rate * 100)

        statistic = {'totalstu': totalstu.count(), 'attend': attend.count(), 'rate': rate}
        return statistic
