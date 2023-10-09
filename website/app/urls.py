from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",views.index,name='index'),
    path("generate",views.generate,name='generate'),
    path("login",views.loginUser,name='login'),
    path("logout",views.logoutUser,name='logout'),
    path("signup",views.signupUser,name='signup'),
    path("home",views.home,name='home'),
    path("profile",views.profile,name='profile'),
    path("passwords",views.passwords,name='passwords'),
    path("store",views.store,name='store'),
    
    ]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)