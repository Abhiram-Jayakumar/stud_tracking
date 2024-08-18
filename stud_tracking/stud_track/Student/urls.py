from django.urls import path

from Student import views

app_name = 'Student'

urlpatterns = [
    
    path('Student_home/', views.Student_home, name='Student_home'),
    path('Login/', views.Login, name='Login'),
    path('view_exam_results/', views.view_exam_results, name='view_exam_results'),
    path('student/<int:student_id>/', views.student_profile, name='student_profile'),
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path('applied_leaves/', views.view_applied_leaves, name='view_applied_leaves'),
    path('uploaded_attendance/', views.view_uploaded_attendance, name='view_uploaded_attendance'),
    path('disciplinary-records/', views.view_disciplinary_records, name='view_disciplinary_records'),
    path('edit/', views.edit_student_details, name='edit_student_details'),
    path('update_password/', views.update_password, name='update_password'),
    path('view_student_payments/', views.view_student_payments, name='view_student_payments'),


                    ]