from django.shortcuts import render, redirect
from account.models import KYC, Account
from django.contrib import messages
from core.forms import CreditCardForm
from core.models import CreditCard,Notification,History,Transaction,DebitCard,TransactionForex
import datetime
from userauths.models import User
from django.db.models import Q
from itertools import chain



def dashboard(request,currency):
    ######### sent transactions ###########

    sent_transaction_all = chain(
        Transaction.objects.filter(sender=request.user, transaction_type='transfer').exclude(
                                                                    Q(transaction_status='Deposit Processing') | 
                                                                    Q(transaction_status='Deposit Completed') | 
                                                                    Q(transaction_type='None') |
                                                                    Q(transaction_status='Withdraw Processing') | 
                                                                    Q(transaction_status='Withdraw Completed') 
                                                                ).order_by('-id'),
        TransactionForex.objects.filter(user=request.user, transaction_type='forex').exclude(
                                                                    Q(transaction_status='Deposit Processing') | 
                                                                    Q(transaction_status='Deposit Completed') | 
                                                                    Q(transaction_type='None') |
                                                                    Q(transaction_status='Withdraw Processing') | 
                                                                    Q(transaction_status='Withdraw Completed') 
                                                                ).order_by('-id'),
    )
    sent_transaction_all_list = list(sent_transaction_all)
    # sent_transaction_all_list_count = len(sent_transaction_all_list)

    sent_transaction = Transaction.objects.filter(sender=request.user,transaction_type='transfer').exclude(
                                                                    Q(transaction_status='Deposit Processing') | 
                                                                    Q(transaction_status='Deposit Completed') | 
                                                                    Q(transaction_type='None') |
                                                                    Q(transaction_status='Withdraw Processing') | 
                                                                    Q(transaction_status='Withdraw Completed') 
                                                                ).order_by('-id')
    sent_transaction_count = len(sent_transaction)

    sent_forex_transaction = TransactionForex.objects.filter(user=request.user, transaction_type='forex').exclude(
                                                                    Q(transaction_status='Deposit Processing') | 
                                                                    Q(transaction_status='Deposit Completed') | 
                                                                    Q(transaction_type='None') |
                                                                    Q(transaction_status='Withdraw Processing') | 
                                                                    Q(transaction_status='Withdraw Completed') 
                                                                ).order_by('-id')
    sent_forex_transaction_count = len(sent_forex_transaction)



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

    #################

    request_sent_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request").order_by('-id')
    request_recieved_transaction = Transaction.objects.filter(reciever=request.user, transaction_type="request").exclude(transaction_status='request_processing').order_by('-id')

    request_sent_transaction_count = request_sent_transaction.count()
    request_recieved_transaction_count = request_recieved_transaction.count()

    month = datetime.datetime.now().month
    year = datetime.datetime.now().year + 5
    

    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.error(request,'You need to sumbit your KYC!')
            return redirect('account:kyc_reg')
        
        account = Account.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user=request.user).order_by('-id')
        debit_card = DebitCard.objects.filter(user=request.user).order_by('-id')


        if request.method == 'POST':
            if account.credit_card_count < 2:
                form = CreditCardForm(request.POST)
                if form.is_valid():
                    new_form = form.save(commit=False)
                    new_form.user = request.user
                    new_form.name = request.user.kyc.full_name
                    # new_form.amount = request.user.account.account_balance
                    new_form.save()

                    credit_card_id = new_form.credit_card_id

                    Notification.objects.create(
                        user=request.user,
                        notification_type="Added Credit Card",
                        card_number = new_form.format_card_number(),
                        card_type = new_form.card_type,
                        card_tier = new_form.card_tier
                    )
                    History.objects.create(
                        user=request.user,
                        history_type="Added Credit Card",
                        card_number = new_form.format_card_number(),
                        card_type = new_form.card_type,
                        card_tier = new_form.card_tier
                    )
                    account.credit_card_count += 1
                    account.save()
                    messages.success(request,'Card Added Successfully.')
                    return redirect('account:dashboard', request.user.account.account_currency)
            else:
                messages.error(request,'You can only have 2 credit cards at a time')
                return redirect('account:dashboard' , request.user.account.account_currency)
        else:
            form = CreditCardForm()

    else:
        messages.error(request,'You need to login to access the dashboard' , request.user.account.account_currency)
        return redirect('userauths:sign_in')
    
    context = {
        'kyc':kyc,
        'account':account,
        'form':form,
        'month':month,
        'year':year,
        'credit_card':credit_card,

        "sent_transaction_all_list":sent_transaction_all_list,
        'sent_transaction_count':sent_transaction_count,
        'sent_forex_transaction_count':sent_forex_transaction_count,

        'recieved_transaction_all_list':recieved_transaction_all_list,
        'recieved_transaction_count':recieved_transaction_count,
        'recieved_forex_transaction_count':recieved_forex_transaction_list_count,


        'request_sent_transaction':request_sent_transaction,
        'request_recieved_transaction':request_recieved_transaction,

        'request_sent_transaction_count':request_sent_transaction_count,
        'request_recieved_transaction_count':request_recieved_transaction_count,
        'debit_card':debit_card,


    }
    return render(request,'account/dashboard.html',context)



def search_user_transactions(request):
    query = None
    transaction_results = []
    if request.method == 'POST':
        my_account = request.user

        query = request.POST.get('search_user_transactions')

        related_users = User.objects.filter(
            Q(username__icontains=query) | Q(kyc__full_name__icontains=query)
        )

        transaction_results = Transaction.objects.filter(
            Q(sender=my_account, reciever__in=related_users) | Q(reciever=my_account, sender__in=related_users)
        ).order_by('-id')

    transaction_results_count = transaction_results.count()

    context = {
        'transaction_results': transaction_results,
        'query': query,
        'transaction_results_count': transaction_results_count,
        'my_account': my_account
    }
    return render(request, 'account/search_user_transactions.html', context)



    # adding debit card from account and dashboard

def add_debit_card(request):
    
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.error(request,'You need to sumbit your KYC!')
            return redirect('account:kyc_reg')
        
        account = Account.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user=request.user).order_by('-id')
        debit_card = DebitCard.objects.filter(user=request.user).order_by('-id')


        if request.method == 'POST':
            if account.credit_card_count < 2:
                form = CreditCardForm(request.POST)
                if form.is_valid():
                    new_form = form.save(commit=False)
                    new_form.user = request.user
                    new_form.name = request.user.kyc.full_name
                    # new_form.amount = request.user.account.account_balance
                    new_form.save()

                    credit_card_id = new_form.credit_card_id

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
                    account.credit_card_count += 1
                    account.save()
                    messages.success(request,'Card Added Successfully.')
                    return redirect('account:dashboard', request.user.account.account_currency)
            else:
                messages.error(request,'You can only have 1 credit cards at a time')
                return redirect('account:dashboard', request.user.account.account_currency)
        else:
            form = CreditCardForm()

    else:
        messages.error(request,'You need to login to access the dashboard', request.user.account.account_currency)
        return redirect('userauths:sign_in')
    