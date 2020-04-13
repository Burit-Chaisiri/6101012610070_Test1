from django.forms import ModelForm
from .models import *

# Create the form class.
#แบบform ของ โปรไฟล์ 
class Profileform(ModelForm):
     class Meta:
        model = Profile
        fields = ['profilePicture']
#แบบform ของ แต่ละLecture 
class LectureForms(ModelForm):
   class Meta:
      model = Lecture
      fields = ['title','description']
#แบบform ของ รูปแต่ละLecture 
class Lecture_imgForms(ModelForm):
      class Meta:
         model = Lecture_img
         fields = ['image']