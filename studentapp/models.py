
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    USER = (
        ('1', 'HOD'),
        ('2', 'STAFF'),
        ('3', 'STUDENT'),
    )
    user_type = models.CharField(choices=USER, max_length=50)
    profile_pic = models.ImageField(upload_to = 'media/profile_pic')



    # def __str__(self):
    #     return self.course_name

class Session_Year(models.Model):
    session_start = models.CharField(max_length=100)        
    session_end = models.CharField(max_length=100)

    
    def __str__(self):
        return self.session_start + " To " + self.session_end 


class Staff(models.Model):
    admin =  models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    qualification = models.TextField()
    address = models.TextField()
    gender = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_image = models.ImageField(upload_to = 'media/staff/profile_pic')

   
    def __str__(self):
        return self.admin.username

   
    
class category(models.Model):
    category_name=models.CharField(max_length=90)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.category_name 
 

class Course(models.Model):
    owner = models.ForeignKey(to=CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    staff_id=models.ForeignKey(to=Staff,on_delete=models.CASCADE,null=True,blank=True)
    course_id = models.IntegerField(primary_key=True)
    couse_category=models.ForeignKey(category,on_delete=models.CASCADE,null=True,blank=True)
    course_name = models.CharField(max_length=100)    
    course_price = models.IntegerField()    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_course_pic = models.ImageField(upload_to = 'media/profile_course_pic')
    course_title = models.CharField(max_length=500)    
    course_description = models.CharField(max_length=500)    

    def __str__(self):
        return self.course_name
    
    

class Student(models.Model):
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)    
    address = models.TextField(null=True,blank=True)
    gender = models.CharField(max_length=100,null=True,blank=True)
    course_id = models.ForeignKey(Course,on_delete=models.DO_NOTHING,null=True,blank=True)
    session_year_id = models.ForeignKey(Session_Year,on_delete=models.DO_NOTHING,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_img = models.ImageField(upload_to = 'media/student/profile_pic',null=True,blank=True)
    category = models.ForeignKey(category,on_delete=models.CASCADE,blank=True,null=True)


    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
    

    def __str__(self):
        return self.admin.username
   


class order(models.Model):

    # name=models.CharField(max_length=70)
    # amount=models.CharField(max_length=70)
    # payment_id=models.CharField(max_length=70)
    # paid=models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    mobile= models.CharField(max_length=100,null=True,blank=True)
    country=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True)
    postal_code =models.IntegerField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    amount = models.CharField(max_length=100,null=True,blank=True)
    payment_id = models.CharField(max_length=300,null=True,blank=True)
    paid = models.BooleanField(default=False,null=True)
    date =models.DateField(auto_now_add=True)
    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    order = models.ForeignKey(order,on_delete=models.CASCADE)
    course = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/Order_Img')
    price = models.CharField(max_length=50)
    total =models.CharField(max_length=1000)
    def __str__(self):
        return self.order.user.username
    
    # price

class Video(models.Model):
    caption = models.CharField(max_length=100)
    video = models.FileField(upload_to="video/%y")
    def __str__(self):
        return self.caption
    