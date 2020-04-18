from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model): # Model ของ โปรไฟล์ของผู้ใช้งาน 
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        default=None,
        null=True
    )
    profilePicture = models.ImageField(upload_to="images/", blank=True, default=None, null=True)  # รูปภาพของ ผู้ใช้งาน 
    def __str__(self):
        return self.user.username # แสดงชื่อไอดีที่ได้สมัครของผู้ใช้งาน username=ชื่อไอดีของผู้ใช้งาน


class Lecture(models.Model): # Model ของ Lecture
    title = models.CharField(max_length=200,null=True) # กล่องข้อความที่ใส่ชื่อชื่อเรื่อง
    subject = models.CharField(max_length=200,null=True) # กล่องข้อความที่ใส่ชื่อวิชา
    description = models.CharField(max_length=2000,null=True)# กล่องข้อความที่ใส่รายละเอียด 
    author = models.ForeignKey(Profile, related_name='author',on_delete=models.CASCADE,blank=True,null=True)
    userSaved = models.ManyToManyField(Profile)
    def __str__(self):
        return self.title
# Model ของ รูปที่อัพพร้อม Lecture
class Lecture_img(models.Model):
    LectureKey = models.ForeignKey(Lecture, related_name='Lecture_img',on_delete=models.CASCADE,blank=True,null=True)
    image = models.ImageField(upload_to='lecture_image',blank=True) #ไว้ใส่รูปภาพ
    def __str__(self):
        return self.image.name

    
