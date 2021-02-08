from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from face_recognition_data.models import UserList, AttendanceSheet, FaceData


class UserListAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('user_id', 'user_name', 'entry_time', 'modify_time', 'photo_img')
    list_filter = ('user_id', 'user_name', 'modify_time')

    def photo_img(self, obj):
        return mark_safe('<img src="{}" height="64" width="64" style="border-radius:50%"/>'.format(obj.photo.url))

    photo_img.short_description = '用户人脸照片'
    photo_img.allow_tags = True


class AttendanceSheetAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('user', 'attendance_time', 'attendance_statu', 'attendance_img')
    list_filter = ('attendance_time', 'attendance_statu')

    def attendance_img(self, obj):
        return mark_safe('<img src="{}" height="64" width="64" style="border-radius:50%"/>'.format(obj.attendance.url))

    attendance_img.short_description = '签到照片'
    attendance_img.allow_tags = True


class FaceDataAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'face_data')
    list_filter = ('user_id', )
    readonly_fields = ('user_id', 'face_data', )


admin.site.register(UserList, UserListAdmin)
admin.site.register(AttendanceSheet, AttendanceSheetAdmin)
admin.site.register(FaceData, FaceDataAdmin)

admin.site.site_header = '人脸识别签到系统'
admin.site.site_title = '人脸识别签到系统后台'
admin.site.index_title = '人脸识别签到系统后台管理'
