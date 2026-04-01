from django.contrib import admin
from django.urls import path
from taskapp import views
from .views import create_task

urlpatterns = [
    
    path("", views.admindashboard, name='admindashboard'),
    path("create_task", views.create_task, name='create_task'),
    path("details/<int:id>", views.details, name='details'),
    path("userdetails/<int:id>", views.userdetails, name='userdetails'),
    path("assigntask", views.assigntask, name='assigntask'),
    path("pending", views.pending, name='pending'),
    path("userdashboard", views.userdashboard, name='userdashboard'),
    path("userpending", views.userpending, name='userpending'),
    path("resolved", views.resolved, name='resolved'),
    path("userresolved", views.userresolved, name='userresolved'),
    path('login',views.login_view, name='login'),
    path("Logout_page",views.Logout_page, name='Logout'),
    # path('networking_admin_dashboard', views.networking_admin_dashboard, name='networking_admin_dashboard'),
    # path('software_admin_dashboard', views.software_admin_dashboard, name='software_admin_dashboard'),
    
]
