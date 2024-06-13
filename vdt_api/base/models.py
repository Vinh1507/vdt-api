from django.db import models

# Create your models here.

class Student(models.Model):
    full_name = models.CharField(max_length=200, blank=False)
    gender = models.CharField(max_length=255, null=True)
    school = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = 'vdt_students'
        
    def __str__(self) -> str:
        return self.full_name
    
class VdtUser(models.Model):
    username = models.CharField(max_length=255, blank=False)
    password = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=15, null=True, blank=True)
    full_name = models.CharField(max_length=200, blank=False)
    class Meta:
        db_table = 'vdt_users'
        
    def __str__(self) -> str:
        return self.username

