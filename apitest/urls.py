from django.urls import path
from . import views

app_name = 'apitest'
urlpatterns = [
    
    path('', views.apitest, name='apitest'),
    path('getdata/', views.getdata, name='getdata'),
    
]