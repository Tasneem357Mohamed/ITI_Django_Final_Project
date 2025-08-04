from django.urls import path
from . import views

urlpatterns = [
    path('' , views.index , name='home'),
    path('register/' , views.register , name='register'),
    path('my-login', views.my_login , name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/' , views.my_logout , name='logout'),
    path('create-record/' , views.create_record , name='create-record'),
    path('view-record/<int:record_id>' , views.view_record , name='view-record'),
    path('update-record/<int:record_id>/', views.update_record, name='update-record'),
    path('delete-record/<int:record_id>/', views.delete_record, name='delete-record'),
]