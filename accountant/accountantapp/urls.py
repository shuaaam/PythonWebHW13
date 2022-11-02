from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('new_category/', views.new_category, name='new_category'),
    path('new_action/', views.new_action, name='new_action'),
    path('detail/', views.detail, name='detail'),
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
]