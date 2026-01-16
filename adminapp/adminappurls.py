from adminapp import views
from django.contrib import admin
from django.urls import path
app_name='adminapp'

urlpatterns = [
   path('',views.adminhome,name='adminhome'),
   path('adminhome',views.adminhome,name='adminhome'),
   path('adminlogiut',views.adminlogout,name='adminlogout'),
   path('addstaff/',views.addstaff,name='addstaff'),
   path('viewstaffrequest/', views.viewstaffrequest, name='viewstaffrequest'),
   path('acceptstaffrequest/<int:id>/', views.acceptstaffrequest, name='acceptstaffrequest'),
   path('deletestaffrequest/<int:id>/', views.deletestaffrequest, name='deletestaffrequest'),
   path('viewdoctorrequest/',views.viewdoctorrequest,name='viewdoctorrequest'),
   path('adddoctor/',views.adddoctor,name='adddoctor'),
   path('acceptdoctorrequest/<int:id>/', views.acceptdoctorrequest, name='acceptdoctorrequest'),
   path('deletedoctorrequest/<int:id>/', views.deletedoctorrequest, name='deletedoctorrequest'),
   path('viewdoctor/',views.viewdoctor,name='viewdoctor'),
   path('viewstaff/',views.viewstaff,name='viewstaff'),
   path('viewcomplaints/', views.viewcomplaints, name='viewcomplaints'),
   path('deletecomplaint/<int:id>/', views.deletecomplaint, name='deletecomplaint'),
   path('addnotification/',views.addnotification,name='addnotification'),
   path('viewnotifi/',views.viewnotifi,name='viewnotifi'),
   path('deletenotification/<int:id>/', views.deletenotification, name='deletenotification'),
path('dkp/<str:doctor_id>/', views.dkp, name='dkp'),
   path('deletestaff/<int:id>/', views.deletestaff, name='deletestaff'),




   



]