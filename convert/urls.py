from django.urls import path

from convert import views

urlpatterns = [
    path('<currency_1>/<currency_2>/<amount_of_currency_1>/', views.convert),
]
