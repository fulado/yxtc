from django.urls import path
from . import views

urlpatterns = [
    path('check_code/', views.check_code),
    path('login_handle/', views.login_handle),
    path('logout/', views.logout),
    path('main/', views.main),
    path('account/', views.account),
    path('verify/', views.verify),
    path('vehicle/', views.vehicle),
    path('vehicle_modify/', views.vehicle_modify),
    path('verify_modify/', views.verify_modify),
    path('account_add/', views.account_add),
    path('account_modify/', views.account_modify),
    path('account_delete/', views.account_delete),
    path('is_user_exist/', views.is_user_exist),
    path('', views.login),
]
