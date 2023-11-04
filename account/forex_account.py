from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
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
import random
from django.db.models import Q
from account.mixins import MessageHandler
from userauths.models import User






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

    sent_forex_transaction = chain(
        TransactionForex.objects.filter(user=request.user, transaction_type='forex').exclude(
                                                                    Q(transaction_status='Deposit Processing') | 
                                                                    Q(transaction_status='Deposit Completed') | 
                                                                    Q(transaction_status='None') |
                                                                    Q(transaction_status='Withdraw Processing') | 
                                                                    Q(transaction_status='Withdraw Completed') 
                                                                ).order_by('-id')

    ) 
    sent_forex_transaction_list = list(sent_forex_transaction)                                              
    sent_forex_transaction_list_count = len(sent_forex_transaction_list)

    recieved_forex_transaction = chain (
        TransactionForex.objects.filter(account_number=request.user.account.account_number).exclude(
                                                                    Q(transaction_status='Deposit Processing') | 
                                                                    Q(transaction_status='Deposit Completed') | 
                                                                    Q(transaction_status='None') |
                                                                    Q(transaction_status='Withdraw Processing') | 
                                                                    Q(transaction_status='Withdraw Completed') |
                                                                    Q(transaction_status='Forex Sent Failed') 
                                                                ).order_by('-id'),
        TransactionForex.objects.filter(account_number=request.user.accountforex.account_number).exclude(
                                                                    Q(transaction_status='Deposit Processing') | 
                                                                    Q(transaction_status='Deposit Completed') | 
                                                                    Q(transaction_status='None') |
                                                                    Q(transaction_status='Withdraw Processing') | 
                                                                    Q(transaction_status='Withdraw Completed') |
                                                                    Q(transaction_status='Forex Sent Failed') 

                                                                ).order_by('-id'),
    )
    recieved_forex_transaction_list = list(recieved_forex_transaction)
    recieved_forex_transaction_list_count = len(recieved_forex_transaction_list)

    for r in recieved_forex_transaction_list:
        print(f"recieved_forex_transaction_list = {r.transaction_status}")


    forex_deposit = chain(
        TransactionForex.objects.filter(user=request.user,transaction_status='Deposit Processing'),
        TransactionForex.objects.filter(user=request.user,transaction_status='Deposit Completed')
    )
    forex_deposit_list = list(forex_deposit)
    forex_deposit_list_count = len(forex_deposit_list)


    forex_withdraw = chain(
        TransactionForex.objects.filter(user=request.user,transaction_status='Withdraw Processing'),
        TransactionForex.objects.filter(user=request.user,transaction_status='Withdraw Completed')
    )
    forex_withdraw_list = list(forex_withdraw)
    forex_withdraw_list_count = len(forex_withdraw_list)

    





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

        'sent_forex_transaction_list':sent_forex_transaction_list,
        'sent_forex_transaction_list_count':sent_forex_transaction_list_count,

        'recieved_forex_transaction_list':recieved_forex_transaction_list,
        'recieved_forex_transaction_list_count':recieved_forex_transaction_list_count,

        'forex_deposit_list':forex_deposit_list,
        'forex_deposit_list_count':forex_deposit_list_count,

        'forex_withdraw_list':forex_withdraw_list,
        'forex_withdraw_list_count':forex_withdraw_list_count

    }

    print(f"forex_deposit_list= {forex_deposit_list}")

    return render(request,'forex/forex_dashboard.html',context)




def forex_account_details(request):
    user = request.user
    account_forex = AccountForex.objects.get(user=request.user)

    context = {
        'account_forex':account_forex,
        'user':user,

    }

    return render(request,'forex/forex_account_details.html',context)


def change_pin_number_forex(request):
    user = request.user
    kyc = KYC.objects.get(user=user)

    user.otp = random.randint(100000,999999)
    user.save()

    def format_phone_number(phone_number):
        phone_number = phone_number.replace(" ", "")
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        return phone_number
    user.user_id = random.randint(12345678,99999999)
    user.save()
    
    phone_number = format_phone_number(kyc.mobile)

    message_handler = MessageHandler(phone_number,user.otp).send_otp_on_phone()
    messages.success(request,'The OTP to change the forex pin number is sent to your phone number.')
    return redirect('account:forex_pin_change_confirm_otp',user.user_id)


def forex_pin_change_confirm_otp(request,user_id):
    user = User.objects.get(user_id=user_id)
    account_forex = AccountForex.objects.get(user=user)

    if request.method == 'POST':
        user = User.objects.get(user_id=user_id)
        otp_number = request.POST.get('otp_number')

        if otp_number == user.otp:
            messages.get_messages(request).used = True
            new_pin = random.randint(1111,9999)
            account_forex.pin_number = new_pin
            account_forex.save()
            messages.success(request, 'You changed your Pin Succesfully')
            return redirect('account:forex_dashboard')
        else:
            messages.error(request,'Incorrect OTP,Try again.')
    
    context = {
        'user_id':user_id
    }
    
    return render(request,'forex/forex_pin_change_confirm_otp.html',context)



def delete_forex_account(request,id):
    account = AccountForex.objects.get(id=id, user=request.user)


    if request.method == 'POST':
        pin_number = request.POST.get('pin_number')


        if account.account_balance <= 0 and account.deleted_account == False :
                if pin_number == account.pin_number:
                    account.deleted_account = True
                    account.save()
                    logout(request)
                    messages.success(request,'Your Account has been deleted, For any assistance please contact the Customer Service')
                    return redirect('account:dashboard')
                else:
                    messages.error(request,'Incorrect pin number')
                    return redirect('account:forex_account_details')

            
        else:
            messages.error(request,'You have balance amount in one your account, Please move the money first.')
            return redirect('account:forex_account_details')