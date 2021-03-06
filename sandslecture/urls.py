"""sandslecture URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from Homepage import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'), # new
    path('change-password/', views.change_password, name='change_password'),
    path('about/', views.about, name='about'),
    path('help/', views.help, name='help'),
    path('upload/',views.upload,name='upload'),
    path('<int:lecture_id>/', views.save, name='save'),
    path('<int:lecture_id>/delete/', views.delete, name='delete'),
    path('profile/<str:username>/', views.profile, name='profile'),


   # path("Profile/",views.profile555,name='profile555'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


