from django.urls import path

from transact import views

urlpatterns = [
    path('', views.index),
    path('search/', views.search),
    path('pay/', views.pay),
    path('history/', views.record),
    path('notify/', views.notify),
    path('handle/', views.handle_notification),
    path('upgrade/', views.upgrade),
]
