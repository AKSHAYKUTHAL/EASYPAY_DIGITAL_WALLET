from django.urls import path
from account import dashboard,account,recipients,foreign_account,foreign_account_deposit,foreign_account_withdraw

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


    # foreign_account_deposit
    path('foreign_deposit_check_rate',foreign_account_deposit.foreign_deposit_check_rate,name='foreign_deposit_check_rate'),
    path('foreign_deposit_confirm/<transaction_id>/',foreign_account_deposit.foreign_deposit_confirm,name='foreign_deposit_confirm'),
    path('foreign_deposit_confirm_process/<transaction_id>/',foreign_account_deposit.foreign_deposit_confirm_process,name='foreign_deposit_confirm_process'),


    # foreign_account_deposit
    path('foreign_withdraw_check_rate',foreign_account_withdraw.foreign_withdraw_check_rate,name='foreign_withdraw_check_rate'),
    path('foreign_withdraw_confirm/<transaction_id>/',foreign_account_withdraw.foreign_withdraw_confirm,name='foreign_withdraw_confirm'),
    path('foreign_withdraw_confirm_process/<transaction_id>/',foreign_account_withdraw.foreign_withdraw_confirm_process,name='foreign_withdraw_confirm_process')

]


