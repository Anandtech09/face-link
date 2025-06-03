from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class signup_page(models.Model):
    userr=models.ForeignKey(User,on_delete=models.CASCADE)
    f_name=models.CharField(max_length=25,null=True)
    l_name=models.CharField(max_length=15,null=True)
    user_name=models.CharField(max_length=15,null=True)
    department=models.CharField(max_length=18,null=True)
    image=models.ImageField(upload_to='profile_pic/')
    email=models.EmailField(null=True)
    password=models.CharField(max_length=15,null=True)

class fac_sign(models.Model):
    userr=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=25,null=True)
    user_name=models.CharField(max_length=15,null=True)
    department=models.CharField(max_length=18,null=True)
    image=models.ImageField(upload_to='teacher_pic/')
    email=models.EmailField(null=True)
    number=models.IntegerField(null=True)
    password=models.CharField(max_length=15,null=True)

class student_page(models.Model):
    userr=models.ForeignKey(User,on_delete=models.CASCADE)
    adm_no=models.CharField(max_length=12,null=True)
    dob=models.DateField(null=True)
    father=models.CharField(max_length=30,null=True)
    mother=models.CharField(max_length=30,null=True)
    number=models.IntegerField(null=True)
    gender=models.CharField(max_length=8,null=True)
    age=models.IntegerField(null=True)
    income=models.IntegerField(null=True)
    religion=models.CharField(max_length=16,null=True)
    caste=models.CharField(max_length=14,null=True)
    bloodgroup=models.CharField(max_length=8,null=True)
    address=models.TextField(null=True)
    district=models.CharField(max_length=20,null=True)
    state=models.CharField(max_length=25,null=True)
    lang=models.TextField(null=True)
    nation=models.CharField(max_length=30,null=True)

class FaceRecognition(models.Model):
    userr = models.ForeignKey(User, on_delete=models.CASCADE)
    attendance = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('userr', 'date',)

class Scholarship(models.Model):
    name = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)
    eligibility_criteria = models.TextField(null=True)
    yearly_income=models.IntegerField(null=True)
    deadline = models.DateField(null=True)
    link=models.CharField(max_length=50,null=True)
    S_caste=models.CharField(max_length=15,null=True)