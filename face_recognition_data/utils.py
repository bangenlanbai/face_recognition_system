# -*- coding:utf-8  -*-
# @Time     : 2021-01-22 04:20
# @Author   : BGLB
# @Software : PyCharm
# -*- coding:utf-8  -*-
# @Time     : 2021-01-21 01:35
# @Author   : BGLB
# @Software : PyCharm
import base64
import os
import face_recognition


def face_compare(upload_path, photo_file_dict):
    """
    人脸比对方法
    :param upload_path: 刚刚上传的照片
    :param photo_file_dict: 图片库的照片对应的人
    :return:
    """
    user_id_list = []
    testimage_faces = []

    for item in photo_file_dict:
        testimage_faces.append(item["face_data"])
        user_id_list.append(item["user_id"])
    unknow_image = face_recognition.load_image_file(upload_path)
    unknow_encoding_list = face_recognition.face_encodings(unknow_image)
    result_user_id_list = []
    for item in unknow_encoding_list:
        results = face_recognition.compare_faces(testimage_faces, item, tolerance=0.5)
        for i in range(len(user_id_list)):
            if results[i]:
                result_user_id_list.append(user_id_list[i])
                user_id_list.remove(user_id_list[i])
    return result_user_id_list


def create_face_data(face_img_path):
    image = face_recognition.load_image_file(face_img_path)
    encoding = face_recognition.face_encodings(image)[0]

    return encoding


def base64_convert_png(base64_str, save_path):
    imgdata = base64.b64decode(base64_str)
    with open(save_path, 'wb') as f:
        f.write(imgdata)
