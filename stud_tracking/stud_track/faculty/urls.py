from django.urls import path

from faculty import views

app_name = 'faculty'

urlpatterns = [
        path('register/', views.register_student, name='register_student'),
        path('students/', views.student_list, name='student_list'),
        path('register_parent', views.register_parent, name='register_parent'),
        path('enter_exam_result', views.enter_exam_result, name='enter_exam_result'),
        path('add-subjects/', views.add_subjects, name='add_subjects'),
        path('load-subjects/', views.load_subjects, name='load_subjects'),
        path('add-discip-record/', views.add_disciplinary_record, name='add_disciplinary_record'),
        path('faculty_home/', views.faculty_home, name='faculty_home'),
        path('view-leave-applications/', views.view_leave_applications, name='view_leave_applications'),
        path('approve_leave/<int:application_id>/', views.approve_leave, name='approve_leave'),
        path('faculty/profile/', views.faculty_profile, name='faculty_profile'),
        path('edit/', views.edit_profile, name='edit_profile'),
        path('update_password/', views.update_password, name='update_password'),
        path('upload_attendance/', views.upload_attendance, name='upload_attendance'),

          
     ]