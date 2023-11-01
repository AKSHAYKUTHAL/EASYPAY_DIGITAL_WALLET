from django.contrib import admin
from account.models import Account,KYC,AccountForex
from userauths.models import User
from import_export.admin import ImportExportModelAdmin

class AccountAdminModel(ImportExportModelAdmin):
    list_editable = ['account_status', 'account_balance', 'kyc_submitted', 'kyc_confirmed'] 
    list_display = ['user', 'account_number' ,'account_status', 'account_balance', 'kyc_submitted', 'kyc_confirmed'] 
    list_filter = ['account_status']

class KYCAdmin(ImportExportModelAdmin):
    search_fields = ["full_name"]
    list_display = ['user', 'full_name', 'gender', 'identity_type', 'date_of_birth'] 


class AccountForexAdminModel(ImportExportModelAdmin):
    list_editable = ['account_status', 'account_balance'] 
    list_display = ['id','user', 'account_number' ,'account_status', 'account_balance','account_currency','ifsc_code','swift_code'] 
    list_filter = ['account_currency']





admin.site.register(Account, AccountAdminModel)
admin.site.register(KYC, KYCAdmin)
admin.site.register(AccountForex, AccountForexAdminModel)

