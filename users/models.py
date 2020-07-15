from django.db import models

# Create your models here.

class TUser(models.Model):
    userid = models.AutoField(primary_key=True)
    username=models.CharField(max_length=45)
    userpwd=models.CharField(max_length=45)

    class Meta:
        db_table='Tuser'