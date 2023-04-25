from django.urls import path

from sign import views

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('login/', views.login),
    path('profile/', views.profile),
    path('logout/', views.logout),
]
