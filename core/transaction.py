from core.models import Transaction,TransactionForex
from account.models import Account,KYC,AccountForex
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from itertools import chain



def all_transactions(request):
    transactions = Transaction.objects.all()

    context = {
        'transactions':transactions
    }

    return render(request,'transaction/all_transactions.html',context)

@login_required
def transaction_list(request):
    try:
        kyc = KYC.objects.get(user=request.user)
    except:
        messages.error(request,'You need to submit your KYC!')
        return redirect('account:kyc_reg')
    
    sent_transaction_all = chain(
            Transaction.objects.filter(sender=request.user, transaction_type='transfer').order_by('-id'),
            TransactionForex.objects.filter(user=request.user, transaction_type='forex')
        )
    sent_transaction_all_list = list(sent_transaction_all)
    # sent_transaction_all_list_count = len(sent_transaction_all_list)

    sent_transaction = Transaction.objects.filter(sender=request.user,transaction_type='transfer').order_by('-id')
    sent_transaction_count = sent_transaction.count()

    sent_forex_transaction = TransactionForex.objects.filter(user=request.user, transaction_type='forex').order_by('-id')
    sent_forex_transaction_count = sent_forex_transaction.count()

    ######### recieved ###############

    recieved_transaction_all =chain(
        Transaction.objects.filter(reciever=request.user,transaction_type='transfer').exclude(transaction_status='cancelled').order_by('-id'),
        TransactionForex.objects.filter(account_number=request.user.account.account_number),
        TransactionForex.objects.filter(account_number=request.user.accountforex.account_number)
    )
    recieved_transaction_all_list = list(recieved_transaction_all)
    # recieved_transaction_all_list_count = len(recieved_transaction_all_list)

    recieved_transaction = Transaction.objects.filter(reciever=request.user,transaction_type='transfer').exclude(transaction_status='cancelled').order_by('-id')
    recieved_transaction_count = recieved_transaction.count()

    recieved_forex_transaction = TransactionForex.objects.filter(user=request.user, transaction_type='forex').order_by('-id')
    recieved_forex_transaction_count = recieved_forex_transaction.count()


    request_sent_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request").order_by('-id')
    request_recieved_transaction = Transaction.objects.filter(reciever=request.user, transaction_type="request").order_by('-id')

    context = {
        "sent_transaction_all_list":sent_transaction_all_list,
        'sent_transaction_count':sent_transaction_count,
        'sent_forex_transaction_count':sent_forex_transaction_count,

        'recieved_transaction_all_list':recieved_transaction_all_list,
        'recieved_transaction_count':recieved_transaction_count,
        'recieved_forex_transaction_count':recieved_forex_transaction_count,

        'request_sent_transaction':request_sent_transaction,
        'request_recieved_transaction':request_recieved_transaction,
    }


    return render(request,'transaction/transaction_list.html',context)


@login_required
def transaction_detail_sent(request, transaction_id):
    try:
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except Transaction.DoesNotExist:
        transaction = None

    context = {'transaction': transaction}
    return render(request, 'transaction/transaction_detail_sent.html', context)


@login_required
def transaction_detail_received(request, transaction_id):
    try:
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except Transaction.DoesNotExist:
        transaction = None

    context = {'transaction': transaction}
    return render(request, 'transaction/transaction_detail_received.html', context)
