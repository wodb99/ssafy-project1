from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # 초기 데이터 가져오기
    path('get_deposit_products/', views.get_deposit_products),
    path('get_saving_products/', views.get_saving_products),

    # deposit
    path('deposit/', views.deposit_product_list),
    path('deposit/<str:deposit_name>/', views.deposit_detail),
    path('deposit/<str:deposit_name>/option/', views.deposit_option_list),
    path('deposit/<str:deposit_code>/option/<int:option_id>/', views.deposit_option_detail),
    path('bank/deposit/<str:bank_name>/', views.bank_deposit),
    path('like/deposit/<str:deposit_code>/', views.like_deposit),

    # saving
    path('saving/', views.saving_product_list),
    path('saving/<str:saving_name>/', views.saving_detail),
    path('saving/<str:saving_name>/option/', views.saving_option_list),
    path('saving/<str:saving_code>/option/<int:option_id>/', views.saving_option_detail),
    path('bank/saving/<str:bank_name>/', views.bank_saving),
    path('like/saving/<str:saving_code>/', views.like_saving),
]
