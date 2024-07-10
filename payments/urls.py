from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('collect_money/', views.collect_money, name='collect_money'),
    path('transfer_money/', views.transfer_money, name='transfer_money'),
]
