# -*- coding:utf-8  -*-
# @Time     : 2021-01-20 02:06
# @Author   : BGLB
# @Software : PyCharm
from django.urls import re_path
from . import views

app_name = 'face_recognition_data'

urlpatterns = [
    re_path('upload/', views.upload_attendance_img, name='upload'),
    re_path('attendance_all/',views.attendance_statistics,name='statistics')
    # re_path和path的作用都是一样的。只不过re_path是在写url的时候可以用正则表达式，功能更加强大。
    # re_path(r'', views.index, name='face_recognition_data'),
    # re_path(r'upload/',views.upload_attendance_img, name='upload_img')
]
