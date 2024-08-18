from django.urls import path

from Parent import views

app_name = 'Parent'

urlpatterns = [
       
    path('Parent_home/', views.Parent_home, name='Parent_home'),
    path('disciplinary-records/', views.view_disciplinary_records, name='view_disciplinary_records'),
    path('techer_info/',views.techer_info, name="techer_info"),
    path('uploaded_attendance/', views.view_uploaded_attendance, name='view_uploaded_attendance'),
    path('view_exam_results_by_parent/', views.view_exam_results_by_parent, name='view_exam_results_by_parent'),
    path('view_parent_profile/', views.view_parent_profile, name='view_parent_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_password/', views.update_password, name='update_password'),
    path('view_parent_payments/', views.view_parent_payments, name='view_parent_payments'),
    path('make_payment/<int:payment_id>/', views.make_payment, name='make_payment'),

            ]