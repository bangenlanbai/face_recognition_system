from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from face_recognition_data.utils import create_face_data


class UserList(models.Model):
    """
    用户表
    """
    user_id = models.CharField(verbose_name='用户编号', primary_key=True, max_length=20)
    user_name = models.CharField(verbose_name='姓名', max_length=100)
    entry_time = models.DateTimeField(verbose_name='录入时间', auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    photo = models.ImageField('用户照片', upload_to='photo/')

    class Meta:
        verbose_name = '录入用户列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_id


class FaceData(models.Model):
    """
    用户人脸数据
    """
    user = models.ForeignKey(UserList, verbose_name='用户编号', on_delete=models.CASCADE)
    face_data = models.TextField(verbose_name='用户人脸数据', blank=None)

    @staticmethod
    def get_all_photo_encodings():
        user_face_dict = []

        for obj in FaceData.objects.all():
            face_data_list = obj.face_data.split(',')
            face_data_arr = []
            for j in face_data_list:
                face_data_arr.append(float(j))
            user_face_dict.append({"user_id": obj.user_id, "face_data": face_data_arr})
        return user_face_dict

    class Meta:
        verbose_name = '用户人脸数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_id


class AttendanceSheet(models.Model):
    """
    用户签到表
    """
    user = models.ForeignKey(UserList, verbose_name='签到用户编号', on_delete=models.CASCADE)
    attendance_time = models.DateTimeField(verbose_name='签到时间', auto_now_add=True)
    attendance_img = models.ImageField('用户签到照片', upload_to='upload/')
    attendance_statu = models.BooleanField(verbose_name='签到状态', default=False)

    def __str__(self):
        return self.user.user_name

    class Meta:
        verbose_name = '用户签到记录'
        verbose_name_plural = verbose_name


@receiver(post_save, sender=UserList, dispatch_uid="blogpost_post_save")
def my_model_save_handler(sender, instance, created, **kwargs):

    face_data = create_face_data(instance.photo.path)
    face_data = ','.join(str(i) for i in face_data)
    FaceData.objects.get_or_create(user_id=instance.user_id, face_data=face_data)

