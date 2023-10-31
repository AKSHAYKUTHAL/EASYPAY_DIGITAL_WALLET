from django.urls import path
from account import dashboard,account,recipients,foreign_account

app_name = "account"

urlpatterns = [
    path('dashboard/<currency>/',dashboard.dashboard,name='dashboard'),
    path('search_user_transactions',dashboard.search_user_transactions,name='search_user_transactions'),


    # account
    path('',account.account,name='account'),
    path('kyc_reg/',account.kyc_registration,name='kyc_reg'),
    path('delete_account/<id>/',account.delete_account,name='delete_account'),
    path('is_2fa',account.is_2fa ,name='is_2fa'),


    # recipients

    path('recipients',recipients.recipients,name='recipients'),
    path('recipient_transactions/<recipient_id>/',recipients.recipient_transactions,name='recipient_transactions'),


    # foreign account

    path('foreign_account_add',foreign_account.foreign_account_add,name='foreign_account_add'),
    path('foreign_account_create',foreign_account.foreign_account_create,name='foreign_account_create'),
    path('foreign_dashboard/',foreign_account.foreign_dashboard,name='foreign_dashboard'),
    path('foreign_deposit_check_rate',foreign_account.foreign_deposit_check_rate,name='foreign_deposit_check_rate')



]