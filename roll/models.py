from django.db import models

# Create your models here.

class Tstudent(models.Model):
    stuid=models.AutoField(primary_key=True)
    stuno=models.CharField(max_length=50)
    stuname=models.CharField(max_length=50)
    selectcourse=models.ForeignKey('sc.TSelectCourse',
                                   on_delete=models.CASCADE,db_column='scid')
    class Meta:
        db_table='Tstudent'


class Tcalldate(models.Model):
    calldateid=models.AutoField(primary_key=True)
    calldate=models.DateTimeField()
    selectcourse=models.ForeignKey('sc.TSelectCourse',
                                   on_delete=models.CASCADE,db_column='scid')
    class Meta:
        db_table='Tcalldate'

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