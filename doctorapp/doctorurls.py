from doctorapp import views
from django.contrib import admin
from django.urls import path
app_name='doctorapp'

urlpatterns = [
   path('',views.doctorhome,name='doctorhome'),
   path('doctorhome',views.doctorhome,name='doctorhome'),
   path('vpa/',views.vpa,name='vpa'),
   path('markaproove/<int:id>/', views.markaproove, name='markaproove'),
   path('rejectappointment/<int:id>/', views.rejectappointment, name='rejectappointment'),
   path('rescheduleappointment/<int:id>/', views.rescheduleappointment, name='rescheduleappointment'),
   path('completeappointment/<int:id>/', views.completeappointment, name='completeappointment'),
   path('deleteappointment/<int:id>/', views.deleteappointment, name='deleteappointment'),
   path('doctorlogout/',views.doctorlogout,name='doctorlogout'),
   path('viewnotifications/',views.viewnotifications,name='viewnotifications'),
   # path('test-email/', views.test_email, name='test_email'),





 
]