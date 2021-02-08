import os

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from face_recognition_data.models import UserList, AttendanceSheet, FaceData
# Create your views here.
from face_recognition_system.settings import MEDIA_ROOT
from face_recognition_data.utils import base64_convert_png, face_compare


def index(request):

    return render(request, 'facerecognition/index.html',locals())


def upload_attendance_img(request):
    """
    签到视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        # print(1)
        img_base64 = str(request.POST.get('img_data')).split(',')[1]
        temp_img_path = os.path.join(MEDIA_ROOT, 'test.png').replace('/','\\')
        base64_convert_png(img_base64, temp_img_path)  # base64 转 png
        try:
            user_id = face_compare(temp_img_path, FaceData.get_all_photo_encodings())
        except Exception as e:
            return JsonResponse({"flag": 0, "msg": "未检测到人脸信息， 请重新上传！"})
        if user_id == 0:
            os.remove(temp_img_path)
            return JsonResponse({"flag": 0, "msg": "未匹配到您的人脸信息， 请重新上传！"})

        att_user = AttendanceSheet.objects.filter(user_id=user_id).first()

        if att_user:
            if att_user.attendance_statu:
                os.remove(temp_img_path)
                return JsonResponse({"flag": 1, "msg": "{}重复签到".format(att_user.user.user_name)})
        att_user = AttendanceSheet(user_id=user_id, attendance_statu=True)
        att_user.attendance_img.save(name='{}.png'.format(int(timezone.now().timestamp())), content=open(temp_img_path, 'rb'))
        att_user.save()
        os.remove(temp_img_path)
        return JsonResponse({"flag": 1, "msg": "{}签到成功".format(att_user.user.user_name)})


def attendance_statistics(request):
    """
    签到统计
    :param request:
    :return:
    """
    att_user = AttendanceSheet.objects.all()

    all_user = UserList.objects.all()

    no_att_user_id_list = list(set(item.user_id for item in all_user)-set(item.user_id for item in att_user))

    no_att_user = UserList.objects.filter(user_id__in=no_att_user_id_list)
    # print(no_att_user_id_list)

    return render(request, 'facerecognition/attendance_book.html', locals())
