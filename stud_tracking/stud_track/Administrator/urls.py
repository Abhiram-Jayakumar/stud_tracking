from django.urls import path

from Administrator import views

app_name = 'Administrator'

urlpatterns = [
       path("index/",views.index,name="index"),
       path('register/', views.register_faculty, name='register_faculty'),
       path('Admin_home/', views.Admin_home, name='Admin_home'),
       path('view_student_details/', views.view_student_details, name='view_student_details'),
       path('add_payment/', views.add_payment, name='add_payment'),
       path('view_student_payments/', views.view_student_payments, name='view_student_payments'),

            ]