from django.shortcuts import render, redirect
from account.models import KYC, Account,AccountForex
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CreditCardForm,ForexDebitCardForm
from core.models import CreditCard,Notification,History,DebitCard,TransactionForex,ForexDebitCard
from account.forms import AccountForexForm
from django.contrib.auth import logout
from decimal import Decimal
import datetime
from itertools import chain
from django.db.models import Q




def forex_account_add(request):
    user = request.user
    account = Account.objects.get(user=user)

    form = AccountForexForm(request.POST)


    context = {
        'account':account,
        'form':form
    }

    return render(request,'forex/forex_account_add.html',context)


def forex_account_create(request):
    user = request.user
    account = Account.objects.get(user=user)

    if request.method == 'POST':
        form = AccountForexForm(request.POST)

        try:
            account_forex = AccountForex.objects.get(user=request.user)
            messages.error(request,'You already have a forex account')

        except AccountForex.DoesNotExist:
            pin_number = request.POST.get('pin_number')

            if pin_number == user.account.pin_number:
                if form.is_valid():
                    account_currency = form.cleaned_data['account_currency']


                    if account_currency == (account.account_currency).upper():
                        messages.error(request,'You already have this currency account.')
                        return redirect('account:forex_account_add')
                    else:
                        new_form = form.save(commit=False)
                        new_form.user = request.user
                        new_form.save()
                        messages.success(request,'You created a Forex Account')
                        return redirect('account:forex_dashboard')
                       
            else:
                messages.error(request,'Incorrect Pin')
                return redirect('account:forex_account_add')
    else:
        form = AccountForexForm()




def forex_dashboard(request):

    sent_forex_transaction = TransactionForex.objects.filter(user=request.user, transaction_type='forex').order_by('-id')
    sent_forex_transaction_count = sent_forex_transaction.count()

    recieved_forex_transaction = chain (
        TransactionForex.objects.filter(account_number=request.user.account.account_number).exclude(
                                                                    Q(transaction_status='Forex Sent Waiting') | 
                                                                    Q(transaction_status='None') | 
                                                                    Q(transaction_status='Forex Sent Processing') | 
                                                                    Q(transaction_status='Forex Sent Failed')
                                                                ),
        TransactionForex.objects.filter(account_number=request.user.accountforex.account_number).exclude(
                                                                    Q(transaction_status='Forex Sent Waiting') | 
                                                                    Q(transaction_status='None') | 
                                                                    Q(transaction_status='Forex Sent Processing') | 
                                                                    Q(transaction_status='Forex Sent Failed')
                                                                ),
    )
    recieved_forex_transaction_list = list(recieved_forex_transaction)
    recieved_forex_transaction_list_count = len(recieved_forex_transaction_list)


    





    user = request.user
    kyc = KYC.objects.get(user=user)
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year + 5
    forex_debit_card = ForexDebitCard.objects.filter(user=request.user).order_by('-id')
    form = ForexDebitCardForm(request.POST)


    try:
        account_forex = AccountForex.objects.get(user=user)
    except AccountForex.DoesNotExist:
        messages.error(request,'You dont have a Forex account,Please create one, then proceed')
        return redirect('account:forex_account_add')
    

    if request.method == 'POST':
        if account_forex.debit_card_count < 1:
            form = ForexDebitCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.name = request.user.kyc.full_name
                new_form.amount = account_forex.account_balance
                # new_form.amount = request.user.account.account_balance
                new_form.card_currency = account_forex.account_currency
                new_form.save()

                account_forex.debit_card_count += 1
                account_forex.save()

                debit_card_id = new_form.debit_card_id

                Notification.objects.create(
                    user=request.user,
                    notification_type="Added Debit Card",
                    card_number = new_form.format_card_number(),
                    card_type = new_form.card_type,
                    card_tier = new_form.card_tier
                )
                History.objects.create(
                    user=request.user,
                    history_type="Added Debit Card",
                    card_number = new_form.format_card_number(),
                    card_type = new_form.card_type,
                    card_tier = new_form.card_tier
                )
                messages.success(request,'Forex Debit Card Added Successfully.')
                return redirect('account:forex_dashboard')
        else:
            messages.error(request,'You can only have 1 debit cards at a time')
            return redirect('account:forex_dashboard')
    else:
        form = ForexDebitCardForm()

    

    context = {
        'account_forex':account_forex,
        'user':user,
        'kyc':kyc,
        'year':year,
        'month':month,
        'form':form,
        'forex_debit_card':forex_debit_card,
        'sent_forex_transaction':sent_forex_transaction,
        'recieved_forex_transaction_list':recieved_forex_transaction_list,
    }

    return render(request,'forex/forex_dashboard.html',context)


