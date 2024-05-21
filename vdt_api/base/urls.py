from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('/', views.getRoutes, name='api_list'),
    path('students/', views.getStudents, name='student_list'),
    path('students/update/<id>', views.getUpdateStudent, name='student_update'),
    path('students/create', views.getCreateStudent, name='student_create'),
    path('students/delete/<id>', views.getDeleteStudent, name='student_delete'),
    path('students/<id>', views.getStudentDetail, name='student_get_detail'),
]
