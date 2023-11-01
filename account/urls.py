from django.urls import path
from account import dashboard,account, forex_sent,recipients,forex_account,forex_account_deposit,forex_account_withdraw,forex_debit_card

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


    # forex account
    path('forex_account_add',forex_account.forex_account_add,name='forex_account_add'),
    path('forex_account_create',forex_account.forex_account_create,name='forex_account_create'),
    path('forex_dashboard/',forex_account.forex_dashboard,name='forex_dashboard'),


    # forex_account_deposit
    path('forex_deposit_check_rate',forex_account_deposit.forex_deposit_check_rate,name='forex_deposit_check_rate'),
    path('forex_deposit_confirm/<transaction_id>/',forex_account_deposit.forex_deposit_confirm,name='forex_deposit_confirm'),
    path('forex_deposit_confirm_process/<transaction_id>/',forex_account_deposit.forex_deposit_confirm_process,name='forex_deposit_confirm_process'),


    # forex_account_withdraw
    path('forex_withdraw_check_rate',forex_account_withdraw.forex_withdraw_check_rate,name='forex_withdraw_check_rate'),
    path('forex_withdraw_confirm/<transaction_id>/',forex_account_withdraw.forex_withdraw_confirm,name='forex_withdraw_confirm'),
    path('forex_withdraw_confirm_process/<transaction_id>/',forex_account_withdraw.forex_withdraw_confirm_process,name='forex_withdraw_confirm_process'),


    # forex debit card 
    path('forex_debit_card_detail/<debit_card_id>/',forex_debit_card.forex_debit_card_detail,name='forex_debit_card_detail'),
    path('deactivate_debit_card/<debit_card_id>/',forex_debit_card.deactivate_debit_card,name='deactivate_debit_card'),
    path('delete_debit_card/<debit_card_id>/',forex_debit_card.delete_debit_card,name='delete_debit_card'),



    # forex sent
    path('forex_calculate',forex_sent.forex_calculate,name='forex_calculate'),
    path('forex_account_detail_search',forex_sent.forex_account_detail_search,name='forex_account_detail_search'),



]


