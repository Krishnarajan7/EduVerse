from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.faculty_list, name='faculty_list'),
    path('dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('add-student/', views.add_student, name='add_student'),
    path('update-student/<int:student_id>/', views.update_student, name='update_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('manage-attendance/<int:student_id>/', views.manage_attendance, name='manage_attendance'),
    path('add-marks/<int:student_id>/', views.add_marks, name='add_marks'),
    path('upload-resource/', views.upload_resource, name='upload_resource'),
    path('post-notice/', views.post_notice, name='post_notice'),
    path('edit-notice/<int:notice_id>/', views.edit_notice, name='edit_notice'),
    path('delete-notice/<int:notice_id>/', views.delete_notice, name='delete_notice'),
    path('notices/', views.notice_list, name='notice_list'),
]