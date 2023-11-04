from django.shortcuts import render, redirect
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from core.models import Transaction,Notification,CreditCard,History,TransactionForex
import time
from decimal import Decimal


def notification_detail(request,nid):
    try:
        notification = Notification.objects.get(nid=nid, user=request.user)

        notification.delete()
    except Notification.DoesNotExist:
        messages.error(request, 'Your Notification is removed,For more information check the History')
        return redirect('account:dashboard')

    if notification.transaction_id:
        try:
            transaction = Transaction.objects.get(transaction_id=notification.transaction_id)
        except:
            transaction = TransactionForex.objects.get(transaction_id=notification.transaction_id)
    else:
        transaction = None

    # if notification.card_number:
    #     credit_card = CreditCard.objects.get(number=notification.card_number)
    # else:
    #     credit_card = None

    
    context = {
        'notification':notification,
        'transaction':transaction,
        # 'credit_card':credit_card,
    }
    
    return render(request,'notificaton_and_history/notification_detail.html',context)
    

def history_detail(request,nid):
    try:
        history = History.objects.get(nid=nid, user=request.user)
        history.is_read = True
        history.save()       
    except:
        messages.error(request, 'An Error Occured')
        return redirect('account:dashboard')

    try:
        transaction = Transaction.objects.get(transaction_id=history.transaction_id)
    except Transaction.DoesNotExist:
        transaction = None

    # if notification.card_number:
    #     credit_card = CreditCard.objects.get(number=notification.card_number)
    # else:
    #     credit_card = None

    
    context = {
        'history':history,
        'transaction':transaction,
        # 'credit_card':credit_card,
    }
    
    return render(request,'notificaton_and_history/history_detail.html',context)


def all_history(request):
    all_history = History.objects.filter(user=request.user)
    transactions = [] 
    credit_cards = []

    

    for history in all_history:
        try:
            credit_cards += list(CreditCard.objects.filter(number=history.card_number))
        except CreditCard.DoesNotExist:
            credit_cards = None

    for history in all_history:
        try:
            transactions += list(Transaction.objects.filter(transaction_id=history.transaction_id))
        except Transaction.DoesNotExist:
            transactions = None




    context = {
        'all_history':all_history,
        'transactions':transactions,
        'credit_cards':credit_cards
    }
    return render(request,'notificaton_and_history/all_history.html',context)



def delete_all_notifications(request):
    user = request.user
    try:
        notifications = Notification.objects.filter(user=user)
        notifications.delete()
        messages.success(request, 'Deleted all notifications. For more information, check History.')
    except Notification.DoesNotExist:
        messages.error(request, 'No notifications found.')

    return redirect(request.META.get('HTTP_REFERER'))
