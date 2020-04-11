from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm , PasswordChangeForm
from django.contrib.auth import logout, authenticate, login , update_session_auth_hash
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import *
from .models import Lecture,Profile,Lecture_img
from django.forms import modelformset_factory
from django.http import Http404
from django.db.models import Count
from django.contrib import messages

class NoteWithThumbnail:
    def __init__(self, note, thumbnail):
        self.note = note
        self.thumbnail = thumbnail
# Create your views here.

def signup(request): # สมัครไอดีที่จะเข้าใช้งาน
    if request.method == 'POST': # ถ้า method ที่ได้มามีค่าเป็น POST 
        form = UserCreationForm(request.POST)  #สร้าง formในการสมัคร
        
        if form.is_valid(): #เช็คว่าในform ถูกต้องมั้ย
            newUser = form.save() #นำค่าที่ไปเก็บไว้
            username = form.cleaned_data.get('username') # นำข้อความที่อยู่ใน text ที่มีไอดีว่า username มาเก็บไว้
            raw_password = form.cleaned_data.get('password1')# นำข้อความที่อยู่ใน text ที่มีไอดีว่า password1 มาเก็บไว้
            Profile.objects.create(user = newUser) #สร้าง Profileขึ้นมา
            user = authenticate(username=username, password=raw_password) #กำหนดว่า user จะมี username กับ pass
            login(request, user)#ทำการlogin โดยใช้userที่สมุคร
            return redirect('login') #ไปยัง html ที่แสดงหน้าการเข้าสู้ระบบ
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form}) # ทำการ render html เพื่อแสดงหน้าสมัครไอดีที่ใช้งาน

def home(request):
    noteWithThumbnail = []
    latestNote = []
    popularNote = []
    if request.GET.get('word'):
        keyword = request.GET.get('word').lower()
        for note in Lecture.objects.all():
            if keyword in note.title.lower() or keyword in note.description.lower():
                noteWithThumbnail.append(NoteWithThumbnail(note, note.Lecture_img.all()[0]))
        return render(request, 'searchresult.html',{'noteWithThumbnail':noteWithThumbnail})
    else:
        for note in Lecture.objects.all().order_by('-id')[:8][::-1]:
            latestNote.append(NoteWithThumbnail(note, note.Lecture_img.all()[0]))
        
        for note in Lecture.objects.annotate(count=Count('userSaved')).order_by('count')[:8][::-1]:
            popularNote.append(NoteWithThumbnail(note, note.Lecture_img.all()[0]))

        return render(request, 'home.html',{'latestNote':latestNote, 'popularNote':popularNote})

def upload(request):
    if Profile.objects.filter(user=request.user):
        files=[]
        profileObj = Profile.objects.get(user=request.user)
        #ImageFormSet=modelformset_factory(Lecture_img,form=Lecture_imgForms, extra=1)
        if request.method == 'POST':
            
                #for file in request.FILES:
               #files.append(request.FILES['form-0-image'])

            LectureForm = LectureForms(request.POST)
            #Imageform = Lecture_imgForms(request.POST,request.FILES['image'])
            if LectureForm.is_valid():
                LectureForm = LectureForm.save(commit=False)
                LectureForm.author = profileObj
                LectureForm.save()

                for i in request.FILES.getlist('image'):
                    photo = Lecture_img.objects.create(LectureKey=LectureForm , image=i)
                    photo.save()

                # redirect to homepage
                return redirect('/')

            else:
                Error="Please choose your file"

        else:
            LectureForm = LectureForms()
            Error=""
        return render(request, 'upload.html',{'LectureForm': LectureForm,"Error":Error})
    else:
        #Http404("Profile does not found")
        raise Http404("Profile does not found")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST,user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user) 
    return render(request,'change_password.html',{'form':form})
def about(request):
    return render(request,'about.html')
def help(request):
    return render(request,'help.html')
def lecture(request,lecture_id):
    if request.method == 'POST':
        profileObj = Profile.objects.get(user = request.user)
        noteObj = Lecture.objects.get(id = int(request.POST.get('noteID')))
        if profileObj not in noteObj.userSaved.all():
            noteObj.userSaved.add(profileObj)
            noteObj.save()
        return HttpResponseRedirect("/" + request.POST.get('noteID'))
    else:
        noteObj = Lecture.objects.get(id = lecture_id)
        imageObjList = noteObj.Lecture_img.all()
        return render(request, 'notedetail.html',{'noteObj': noteObj, "imageObjList": imageObjList})

def profile(request, username):
    userObj = User.objects.get(username = username)
    profileObj = Profile.objects.get(user = userObj)
    if request.method == 'POST':
        form=Profileform(request.POST , request.FILES)
        if form.is_valid():
            profileObj.profilePicture = form.cleaned_data.get('profilePicture')
            profileObj.save()
            
            return HttpResponseRedirect("/profile/"+username)
    else:
        form=Profileform()
        myNote = []
        savedNote = []
        saves = 0
        for note in profileObj.author.all():
            myNote.append(NoteWithThumbnail(note, note.Lecture_img.all()[0]))
            saves += note.userSaved.count()
        for note in Lecture.objects.all():
            if profileObj in note.userSaved.all():
                savedNote.append(NoteWithThumbnail(note, note.Lecture_img.all()[0]))
    return render(request,'profile.html',{'form': form, 'profile': profileObj, 'myNote': myNote, 'savedNote':savedNote, 'saves':saves})
