from django.shortcuts import render
from django.shortcuts import render,HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
import pandas as pd
from sc.models import TSelectCourse, Tterm,Tcourse
from .models import Tstudent, Tcallrec,Tcalldate
import os
import datetime as d
import pymysql
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

# Create your views here.

def getext(filename):
    strlist=filename.split('.')
    return strlist[len(strlist)-1]

def upload(request):
    return render(request,'batimport.html')


def importstu(request):
    if request.method == "POST":
        file = request.FILES.get('stulist')
        print(file.name)
        type_excel = getext(file.name)
        print(type_excel)
        if 'xlsx' == type_excel or 'xls'==type_excel:
            stulist=pd.read_excel(file)
            rows=len(stulist)
            termid=request.session.get('termid')
            courseid=request.session.get('courseid')
            term = Tterm.objects.get(termid=termid)
            course = Tcourse.objects.get(courseid=courseid)
            sc=TSelectCourse.objects.filter(term=term,course=course)
            for i in range(rows):
                stuname=stulist['studentname'][i]
                stuno=stulist['studentid'][i]
                student = Tstudent()
                student.stuno=stuno
                student.stuname=stuname
                student.selectcourse=sc[0]
                student.save()
            return HttpResponseRedirect('/static/popclose.html')


def getstulist(request):
    termid = request.session.get('termid')
    courseid = request.session.get('courseid')
    term=Tterm.objects.get(termid=termid)
    course=Tcourse.objects.get(courseid=courseid)

    sc = TSelectCourse.objects.filter(term=term, course=course)
    scid=sc[0].scid
    stulist=Tstudent.objects.filter(selectcourse=sc[0])
    pagenator=Paginator(stulist,5)
    page=request.GET.get('page')

    try:
        stulist=pagenator.page(page)
    except PageNotAnInteger:
        stulist = pagenator.page(1)
    except (EmptyPage,InvalidPage):
        stulist=pagenator.page(pagenator.num_pages)


    return render(request,'call.html',{'stulist':stulist,'scid':scid})

def precall(request):
    scid= request.session.get('scid')
    context=Tcallrec.InitialSign(scid)
    return render(request,'scall.html',context)

def hiscall(request,calldateid):
    scid=request.session.get('scid')
    context=Tcallrec.callhis(scid,calldateid)

    maxid=context.get('calldateid')
    statistic=Tcallrec.statics(maxid)
    context=dict(context,**statistic)
    return render(request,'hiscall.html',context)


def startcall(request,calldateid):
    print(calldateid)
    with open('roll/lock.dat','w') as files:
        files.write(str(calldateid))
    files.close()
    return HttpResponse('success')

def loadsign(request,calldateid):
    calldate=Tcalldate.objects.get(calldateid=calldateid)
    signlist=Tcallrec.objects.filter(calldate=calldate)
    stusignlist=[]
    for sign in signlist:
        stusignlist.append({'stuno':sign.student.stuno,'stuname':sign.student.stuname,
                            'ip':sign.callip,
                            'course':sign.calldate.selectcourse.course.coursename,
                            'iscall':sign.iscall})
    return JsonResponse(stusignlist,safe=False)

def stusign(request,stuno):
    ip="127.0.0.1"

    path=os.path.dirname(__file__)
    file=path+'/lock.dat'
    print(file)

    if os.path.exists(file):
        calldateid=0
        with open(file) as files:
            calldateid=int(files.readline())
        files.close()
        calldate=Tcalldate.objects.get(calldateid=calldateid)
        sc=calldate.selectcourse
        stu=Tstudent.objects.filter(stuno=stuno,selectcourse=sc)

        if stu.count()==0:
            restext="no"
        else:
            nowtime=d.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            stuid=stu[0].stuid
            iscall=1

            sql="update Tcallrec set iscall="+str(iscall)+", calltime='"+nowtime+"', " \
                "callip='"+ip+"' where calldateid="+str(calldateid)+" and stuid="+str(stuid)+" "
            print(sql)
            db=pymysql.connect('localhost','root','python3020','wsign')
            cursor=db.cursor()
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            restext="ok"
    else:
        restext="end"
    return HttpResponse(restext)

def stopcall(request):
    path=os.path.dirname(__file__)
    file=path+'/lock.dat'
    print(file)
    if os.path.exists(file):
        os.remove(file)
    return  HttpResponse('success')