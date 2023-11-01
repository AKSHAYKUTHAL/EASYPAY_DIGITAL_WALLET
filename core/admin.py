from django.contrib import admin
from core.models import Transaction,CreditCard,Notification,History,DebitCard,TransactionForex,ForexDebitCard


class TransactionAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'transaction_status', 'transaction_type']
    list_display = ['id','user', 'amount','fee', 'transaction_status', 'transaction_type', 'reciever', 'sender']


class CreditCardAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'card_type','card_tier','card_status']
    list_display = ['id','user', 'amount','format_card_number','name','month','year', 'card_type','card_tier','card_status']


class NotificationAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['id','user', 'notification_type', 'amount' ,'date','sender','receiver','is_read']

class HistoryAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['id','user', 'history_type', 'amount' ,'date','sender','receiver','is_read']


class DebitCardAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'card_type','card_tier','card_status']
    list_display = ['id','user', 'amount','format_card_number','name','month','year', 'card_type','card_tier','card_status']

class TransactionForexAdmin(admin.ModelAdmin):
    list_editable = [ 'transaction_status', 'transaction_type']
    list_display = ['id','user', 'original_currency_amount','amount_after_fee','conversion_fee', 'recipient_gets','transaction_status', 'transaction_type', 'reciever','reciever_account_currency', 'sender','sender_account_currency','swift_code','ifsc_code']
    



class ForexDebitCardAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'card_type','card_tier','card_status']
    list_display = ['id','user', 'amount','format_card_number','name','month','year', 'card_type','card_tier','card_status','card_currency']


admin.site.register(Transaction,TransactionAdmin)
admin.site.register(CreditCard,CreditCardAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(History, HistoryAdmin)  
admin.site.register(DebitCard,DebitCardAdmin)
admin.site.register(TransactionForex,TransactionForexAdmin)
admin.site.register(ForexDebitCard,ForexDebitCardAdmin)



