from django.db import models

# Create your models here.
class Tterm(models.Model):
    termid=models.AutoField(primary_key=True)
    termname=models.CharField(max_length=100)

    class Meta:
        db_table='Tterm'

class Tcourse(models.Model):
    courseid=models.AutoField(primary_key=True)
    coursename=models.CharField(max_length=100)

    class Meta:
        db_table='Tcourse'

class TSelectCourse(models.Model):
    scid=models.AutoField(primary_key=True)
    term=models.ForeignKey('Tterm',on_delete=models.CASCADE,db_column='termid')
    course = models.ForeignKey('Tcourse', on_delete=models.CASCADE, db_column='courseid')

    class Meta:
        db_table='TSelectCourse'