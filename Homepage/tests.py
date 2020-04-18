from Homepage.models import *
from django.contrib.auth.models import User
from django.shortcuts import render
from django.test import TestCase
from .forms import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.core.files import File
from sandslecture.settings import BASE_DIR
import os
from pathlib import Path
import glob

class HomePageTest(TestCase):

    def test_adding_new_model_Profile(self): # testการเพิ่ม Profile ของผู้ใช้งาน
        password = 'newPassword' #กำหนดรหัสผ่าน
        newUser = User.objects.create_user('newUser', password) #สร้างผู้ใช้งาน
        newProfile = Profile() #สร้าง Profile 
        newProfile.user = newUser #กำหนดให้ Profile นี้เป็นของ ผู้ใช้งานที่พึ่งสร้างขึ้นมา 
        newProfile.save() #บันทึก
        self.assertEqual('newUser',newProfile.user.username) #เช็คว่า ชื่อของผู้ใช้งานใช่ newUser รึเปล่า
        
    def test_saving_and_retrieving_lecture_title(self): 
        firstLecture = Lecture() #สร้าง note ขึ้นมา
        firstLecture.title = 'The first (ever) lecture title' #ใส่หัวข้อ
        firstLecture.save() #ทำการบันทึก

        secondLecture = Lecture() #สร้าง note ขึ้นมา
        secondLecture.title = 'lecture title the second' #ใส่หัวข้อ
        secondLecture.save() #ทำการบันทึก

        lectures = Lecture.objects.all() #ดึงข้อมูลของ note ทั้งหมดมา
        self.assertEqual(lectures.count(), 2)  #เช็คว่า จำนวนของผู้ใช้งานเท่ากับ 2 รึเปล่า
 
        firstLecture = lectures[0] #กำหนดให้ note อันที่ 1 ชื่อ firstLecture
        secondLecture = lectures[1] #กำหนดให้ note อันที่ 2 ชื่อ  secondLecture
        self.assertEqual(firstLecture.title, 'The first (ever) lecture title') #เช็คว่าชื่อหัวข้อของ note อันที่ 1 ใช่  The first (ever) lecture title รึเปล่า
        self.assertEqual(secondLecture.title, 'lecture title the second') #เช็คว่าชื่อหัวข้อของ note อันที่ 2 ใช่  lecture title the second รึเปล่า
 
    def test_saving_lecture_id_auto_increment_start_at_1(self): 
        firstLecture = Lecture() #สร้าง note ขึ้นมา
        firstLecture.title = 'The first (ever) lecture title' #ใส่หัวข้อ
        firstLecture.save() #ทำการบันทึก

        secondLecture = Lecture() #สร้าง note ขึ้นมา
        secondLecture.title = 'lecture title the second' #ใส่หัวข้อ
        secondLecture.save() #ทำการบันทึก

        lectures = Lecture.objects.all() #ดึงข้อมูลของ note ทั้งหมดมา
        self.assertEqual(lectures.count(), 2)  #เช็คว่า จำนวนของผู้ใช้งานเท่ากับ 2 รึเปล่า

        firstLecture = lectures[0] #กำหนดให้ note อันที่ 1 ชื่อ firstLecture
        secondLecture = lectures[1] #กำหนดให้ note อันที่ 2 ชื่อ  secondLecture
        self.assertEqual(firstLecture.id, 1) #เช็คว่า Id ของ note อันที่ 1 เท่ากับ 1 รึเปล่า
        self.assertEqual(secondLecture.id, 2) #เช็คว่า Id ของ note อันที่ 2 เท่ากับ 2 รึเปล่า

    def test_upload_pic_Profile(self):
        c = Client() #ผู้ใช้งาน
        form=Profileform() #สร้าง Profileขึ้นมา
        localtion=BASE_DIR #ระบุตำแหน่งที่เก็บของ รูปภาพ
        Tim=User.objects.create_user(username='Timmy',password='2542') #สร้างผู้ใช้งาน
        ProfileTim=Profile.objects.create(user=Tim) #สร้าง Profile ของผู้ใช้งาน
        response = c.post('/profile/'+str(ProfileTim)+'/', {'profilePicture':SimpleUploadedFile('666.png', content=open(localtion+'/red.png', 'rb').read())} ) #อัพโหลด รูป Profile
        Count_object=Profile.objects.filter(id=1)[0].profilePicture 

        self.assertNotEquals(Count_object,"<ImageFieldFile: None>") #เช็คว่า จำนวนของรูป Profile ไม่เท่ากับ None รึเปล่า





    def test_submit_Lecture(self):
        c = Client()  #ผู้ใช้งาน
        localtion=BASE_DIR  #ระบุตำแหน่งที่เก็บของ รูปภาพ
        Tim=User.objects.create_user(username='Timmy',password='2542') #สร้างผู้ใช้งาน
        ProfileTim=Profile.objects.create(user=Tim) #สร้าง Profile ของผู้ใช้งาน
        self.client.post('/accounts/login/', {'username':'Timmy','password':"2542" } ) #ทำการ login ผู้ใช้งาน
        self.client.post('/upload/', {'title':'tim','description':"555" ,'image':SimpleUploadedFile('666.png', content=open(localtion+'/red.png', 'rb').read())} ) #ทำการอัพโหลด note โดยใส่ชื่อหัวข้อ รายละเอียด รูปภาพ
        CountLec=Lecture.objects.count() #เก็บค่าของจำนวน note ทั้งหมด
        Count_object=Lecture_img.objects.count() #เก็บค่าของจำนวน รูปภาพของnote ทั้งหมด

        self.assertEqual(CountLec,1) #เช็คว่าจำนวน note เท่ากับ 1 รึเปล่า
        self.assertEqual(Count_object,1) #เช็คว่าจำนวน รูปภาพของnote เท่ากับ 1 รึเปล่า


    def test_upload_Muti_Pic_Lecture(self):
        c=Client() #ผู้ใช้งาน
        localtion=BASE_DIR #ระบุตำแหน่งที่เก็บของ รูปภาพ
        Tim=User.objects.create_user(username='tim',password='pass')#สร้างผู้ใช้งาน
        ProfileTim=Profile.objects.create(user=Tim) #สร้าง Profile ของผู้ใช้งาน

        self.client.post('/accounts/login/', {'username':'tim','password':"pass" } ) #ทำการ login ผู้ใช้งาน
        self.client.post('/upload/', {'submitbutton':'Submit','title':'tim','description':"555" ,'image':{SimpleUploadedFile('666_1.png', content=open(localtion+'/red.png', 'rb').read()),SimpleUploadedFile('666_1.png', content=open(localtion+'/red.png', 'rb').read())}} )#ทำการอัพโหลด note โดยใส่ชื่อหัวข้อ รายละเอียด รูปภาพ 2 รูป
        self.assertEqual(Lecture.objects.count(),1) #เช็คว่าจำนวน note เท่ากับ 1 รึเปล่า
        self.assertEqual(Lecture_img.objects.count(),2)#เช็คว่าจำนวน รูปภาพของnote เท่ากับ 2 รึเปล่า

    
    def test_saves_Lecture(self):
        creator = User.objects.create_user(username = 'tim01',password = 'pass') #สร้างผู้ใช้งาน
        userB = User.objects.create_user(username = 'tim21',password = 'pass')#สร้างผู้ใช้งาน
        userA = User.objects.create_user(username = 'tim11',password = 'pass') #สร้างผู้ใช้งาน
        creatorProfile = Profile.objects.create(user = creator) #สร้าง Profile ของผู้ใช้งาน
        
        userAProfile = Profile.objects.create(user = userA) #สร้าง Profile ของผู้ใช้งาน
        
        userBProfile = Profile.objects.create(user = userB) #สร้าง Profile ของผู้ใช้งาน
        noteObj = Lecture.objects.create(title = 'test', description = 'test',author = creatorProfile) #สร้าง note
        
        useA=noteObj.userSaved.add(userAProfile) #ทำการบันทึก note
        
        self.assertEqual(noteObj.userSaved.count(),1) #เช็คว่าจำนวนการถูกบันทึกของ note มีค่าเท่ากับ 1 รึเปล่า
        self.assertIn(userAProfile,Lecture.objects.all()[0].userSaved.all()) #เช็คว่าใน savenote มีnoteที่ถูกบันทึกไปรึเปล่า 
        useB=noteObj.userSaved.add(userBProfile) #ทำการบันทึก note
        
        self.assertEqual(noteObj.userSaved.count(),2) #เช็คว่าจำนวนการถูกบันทึกของ note มีค่าเท่ากับ 2 รึเปล่า
        self.assertIn(userBProfile,Lecture.objects.all()[0].userSaved.all())#เช็คว่าใน savenote มีnoteที่ถูกบันทึกไปรึเปล่า 

    def test_search_Lecture(self):
        creator = User.objects.create_user(username = 'tim01',password = 'pass') #สร้างผู้ใช้งาน
        creatorProfile = Profile.objects.create(user = creator) #สร้าง Profile ของผู้ใช้งาน
        noteObj = Lecture.objects.create(title = 'test', description = 'test',author = creatorProfile) #สร้าง note
        noteObj_Img=Lecture_img.objects.create(LectureKey=noteObj,image=SimpleUploadedFile('666_1.png', content=open(BASE_DIR+'/red.png', 'rb').read()))#สร้างรูปภาพ
        response = self.client.get('/',{'word':'test'}) #ทำการใส่ข้อความเพื่อ search ว่า test
        y=response.content.decode()

        self.assertEqual(response.status_code,200)
        self.assertIn('test',y) #เช็คว่ามี test อยู่ในระบบมั้ย
    def test_change_password(self):
        creator = User.objects.create_user(username = 'tim01',password = 'pass') #สร้างผู้ใช้งาน
        creatorProfile = Profile.objects.create(user = creator) #สร้าง Profile ของผู้ใช้งาน
        self.client.login(username = 'tim01',password = 'pass') #ทำการ login เข้าไป
        self.client.post('/change-password/',{"old_password":'pass',"new_password1":"time25422542","new_password2":"time25422542"}) #เปลี่ยนรหัสผ่าน
        self.client.logout() # ออกจากระบบ
        Login_test_new_pass=self.client.post('/accounts/login/', {'username':'tim01','password':"time25422542" },follow=True )  #login โดยรหัสผ่านใหม่
        
        self.assertEqual(Login_test_new_pass.status_code,200)
        self.assertIn("tim01",Login_test_new_pass.content.decode())

    
    def test_Lecture_show_on_home(self):
        localtion=BASE_DIR #ระบุตำแหน่งที่เก็บของ รูปภาพ
        Tim=User.objects.create_user(username='Timmy',password='2542') #สร้างผู้ใช้งาน
        ProfileTim=Profile.objects.create(user=Tim) #สร้าง Profile ของผู้ใช้งาน
        self.client.post('/accounts/login/', {'username':'Timmy','password':"2542" } )  #ทำการ login เข้าไป
        upload=self.client.post('/upload/', {'title':'tim','description':"555" ,'image':SimpleUploadedFile('666.png', content=open(localtion+'/red.png', 'rb').read())} ) #อัพโหลด note

        home=self.client.post('/').content.decode()

        self.assertIn('666.png',home) #มีรูป note อยู่ในหน้า home มั้ย
        self.assertIn('tim',home) # มีชื่อหัวข้อ note อยู่ในหน้า home มั้ย
        #self.assertEqual(Count_object,1)

    def test_Lecture_show_on_Profile(self):    
        localtion=BASE_DIR #ระบุตำแหน่งที่เก็บของ รูปภาพ
        Tim=User.objects.create_user(username='Timmy',password='2542') #สร้างผู้ใช้งาน
        ProfileTim=Profile.objects.create(user=Tim) #สร้าง Profile ของผู้ใช้งาน
        self.client.post('/accounts/login/', {'username':'Timmy','password':"2542" } )  #ทำการ login เข้าไป
        upload=self.client.post('/upload/', {'title':'tim','description':"555" ,'image':SimpleUploadedFile('666.png', content=open(localtion+'/red.png', 'rb').read())} )  #อัพโหลด note
        Profile_page=Client().post('/profile/Timmy/',follow=True).content.decode()

        self.assertIn('666.png',Profile_page) # มีรูป note อยู่ในหน้า Profile มั้ย
        self.assertIn('tim',Profile_page)  # มีชื่อหัวข้อ note อยู่ในหน้า Profile มั้ย

    def tearDown(self):
        for i in glob.glob(BASE_DIR+'/sandslecture/media/*'):
            i=Path(i)
            for file in i.glob('666*.png'):
                os.remove(file)

        
        


       