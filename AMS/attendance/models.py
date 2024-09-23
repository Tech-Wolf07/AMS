from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Admin(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=10)
    def __str__(self):
        return self.user.username
    
class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=20,unique=True)
    role = models.CharField(max_length=10)
    course = models.ManyToManyField('course')

    def __str__(self):
        return self.user.username
    
class Students(models.Model):
    name = models.CharField(max_length=20)
    rollno = models.IntegerField(null=True)
    Students_class = models.CharField(max_length=10)

    def __str__(self):
        return {self.name},{self.rollno},{self.Students_class}
    
class Course(models.Model):
    cname = models.CharField(max_length=50)
    Admin = models.ForeignKey(Admin,on_delete=models.CASCADE)
    Teacher = models.ManyToManyField(Teacher,related_name='courses')

    def __str__(self):
        return self.cname
    
class Profile(models.Model):
    user = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.user.name

class Attendance(models.Model):
    student = models.ForeignKey(Students,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)    
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10,choices=[('Present','Present'),('Absent','Absent')]) 

    def __str__(self):
        return f"{self.student.name} - {self.course.cname} - {self.date} - {self.status}"
       

