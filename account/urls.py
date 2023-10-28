from django.urls import path
from account import views

app_name = "account"

urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.account,name='account'),
    path('kyc_reg/',views.kyc_registration,name='kyc_reg'),
    path('delete_account/<id>/',views.delete_account,name='delete_account'),
    path('is_2fa',views.is_2fa ,name='is_2fa'),
    path('search_user_transactions',views.search_user_transactions,name='search_user_transactions'),
    path('recipients',views.recipients,name='recipients'),
    path('recipient_transactions/<recipient_id>/',views.recipient_transactions,name='recipient_transactions'),


]