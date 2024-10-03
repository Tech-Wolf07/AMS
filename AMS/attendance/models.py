from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Admin(models.Model):
    name = models.CharField(max_length=20,unique=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=10)
    def __str__(self):
        return self.user.name
    
class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=20,unique=True)
    role = models.CharField(max_length=10)
    course = models.ManyToManyField('course')

    def __str__(self):
        return self.user.username
    
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

class Add_class(models.Model):
    class_name = models.CharField(max_length=30)
    Teacher = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True)

    
class Students(models.Model):
    name = models.CharField(max_length=20)
    rollno = models.IntegerField(null=True)
    Students_class = models.CharField(max_length=10)

    #def __str__(self):
    #    return {self.name},{self.rollno},{self.Students_class}

class Attendance(models.Model):
    student = models.ForeignKey(Students,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)    
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10,choices=[('Present','Present'),('Absent','Absent')]) 

    def __str__(self):
        return f"{self.student.name} - {self.course.cname} - {self.date} - {self.status}"


class Report(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_classes = models.IntegerField()
    total_present = models.IntegerField()
    total_absent = models.IntegerField()
    
    def __str__(self):
        return f"Report for {self.student.name} - {self.course.cname}"

    def calculate_attendance(self):
        # Example function to calculate attendance within the date range
        attendance_records = Attendance.objects.filter(
            student=self.student,
            course=self.course,
            teacher=self.teacher,
            date__range=[self.start_date, self.end_date]
        )
        self.total_classes = attendance_records.count()
        self.total_present = attendance_records.filter(status='Present').count()
        self.total_absent = attendance_records.filter(status='Absent').count()
        self.save()


