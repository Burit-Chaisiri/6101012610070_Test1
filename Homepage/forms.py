from django.forms import ModelForm
from .models import *

# Create the form class.

class Profileform(ModelForm): #แบบform ของ โปรไฟล์ 
     class Meta:
        model = Profile
        fields = ['profilePicture']


class LectureForms(ModelForm): #แบบform ของ แต่ละLecture 
   class Meta:
      model = Lecture
      fields = ['title','description']

class Lecture_imgForms(ModelForm): #แบบform ของ รูปแต่ละLecture 
      class Meta:
         model = Lecture_img
         fields = ['image']