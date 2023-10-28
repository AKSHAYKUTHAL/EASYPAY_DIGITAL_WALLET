from django.shortcuts import render, redirect
from account.models import KYC, Account
from account.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CreditCardForm
from core.models import CreditCard,Notification,History,Transaction,DebitCard
import datetime
from django.contrib.auth import authenticate,login,logout
from userauths.models import User
from django.db.models import Q
from django.db.models import Count




def account(request): 
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.error(request,'You need to submit your KYC!')
            return redirect('account:kyc_reg')
        
        account = Account.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user=request.user).order_by('-id')
        debit_card = DebitCard.objects.filter(user=request.user).order_by('-id')


        form = CreditCardForm(request.POST)


        month = datetime.datetime.now().month
        year = datetime.datetime.now().year + 5

        
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
                    return redirect('account:account')
            else:
                messages.error(request,'You can only have 2 credit cards at a time')
                return redirect('account:account')
        else:
            form = CreditCardForm()
        

    else:
        messages.error(request,'You need to login to access the dashboard')
        return redirect('userauths:sign_in')
    context = {
        'kyc':kyc,
        'account':account,
        'credit_card':credit_card,
        'month':month,
        'year':year,
        'form':form,
        'debit_card':debit_card,
    }
    return render(request,'account/account.html',context)



def delete_account(request,id):
    account = Account.objects.get(id=id, user=request.user)
    credit_card = CreditCard.objects.filter(user=request.user)

    credit_card_balance = 0

    if request.method == 'POST':
        pin_number = request.POST.get('pin_number')
        
        try:
            for c in credit_card :
                credit_card_balance += c.amount 
        except:
            credit_card_balance = 0


        if account.account_balance <= 0 and account.deleted_account == False :
            if credit_card_balance == 0:

                if pin_number == account.pin_number:
                    account.deleted_account = True
                    account.save()
                    logout(request)
                    messages.success(request,'Your Account has been deleted, For any assistance please contact the Customer Service')
                    return redirect('core:index')
                else:
                    messages.error(request,'Incorrect pin number')
                    return redirect('account:account')
            else:
                messages.error(request,'You have balance amount in one of your cards, Please move the money first,then only try to delete account.')
                return redirect('account:account')
            
        else:
            messages.error(request,'You have balance amount in one your account, Please move the money first.')
            return redirect('')




@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)


    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc = None

    if request.method == 'POST':
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, 'KYC Form submitted successsfully. In review now!')
            account.kyc_submitted = True
            account.save()
            return redirect('core:index')
    else:
        form = KYCForm(instance=kyc)
    context = {
        'account':account,
        'form':form,
        'kyc':kyc,
    }
    return render(request, 'account/kyc_form.html',context)



def dashboard(request):
    sent_transaction = Transaction.objects.filter(sender=request.user,transaction_type='transfer').order_by('-id')
    recieved_transaction = Transaction.objects.filter(reciever=request.user,transaction_type='transfer').exclude(transaction_status='cancelled').order_by('-id')

    sent_transaction_count = sent_transaction.count()
    recieved_transaction_count = recieved_transaction.count()

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
                    return redirect('account:dashboard')
            else:
                messages.error(request,'You can only have 2 credit cards at a time')
                return redirect('account:dashboard')
        else:
            form = CreditCardForm()

    else:
        messages.error(request,'You need to login to access the dashboard')
        return redirect('userauths:sign_in')
    
    context = {
        'kyc':kyc,
        'account':account,
        'form':form,
        'month':month,
        'year':year,
        'credit_card':credit_card,
        "sent_transaction":sent_transaction,
        "recieved_transaction":recieved_transaction,
        'request_sent_transaction':request_sent_transaction,
        'request_recieved_transaction':request_recieved_transaction,

        'sent_transaction_count':sent_transaction_count,
        'recieved_transaction_count':recieved_transaction_count,
        'request_sent_transaction_count':request_sent_transaction_count,
        'request_recieved_transaction_count':request_recieved_transaction_count,
        'debit_card':debit_card,


    }
    return render(request,'account/dashboard.html',context)


def add_debit_card(request):
    sent_transaction = Transaction.objects.filter(sender=request.user,transaction_type='transfer').order_by('-id')
    recieved_transaction = Transaction.objects.filter(reciever=request.user,transaction_type='transfer').exclude(transaction_status='cancelled').order_by('-id')

    sent_transaction_count = sent_transaction.count()
    recieved_transaction_count = recieved_transaction.count()

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
                    return redirect('account:dashboard')
            else:
                messages.error(request,'You can only have 2 credit cards at a time')
                return redirect('account:dashboard')
        else:
            form = CreditCardForm()

    else:
        messages.error(request,'You need to login to access the dashboard')
        return redirect('userauths:sign_in')
    
    context = {
        'kyc':kyc,
        'account':account,
        'form':form,
        'month':month,
        'year':year,
        'credit_card':credit_card,
        "sent_transaction":sent_transaction,
        "recieved_transaction":recieved_transaction,
        'request_sent_transaction':request_sent_transaction,
        'request_recieved_transaction':request_recieved_transaction,

        'sent_transaction_count':sent_transaction_count,
        'recieved_transaction_count':recieved_transaction_count,
        'request_sent_transaction_count':request_sent_transaction_count,
        'request_recieved_transaction_count':request_recieved_transaction_count


    }
    return render(request,'account/dashboard.html',context)


def is_2fa(request):
    user = request.user
    
    if user.is_2fa == True:
        user.is_2fa = False
        user.save()
        messages.success(request,'You disabled the 2FA')
        return redirect('account:account')
    else:
        user.is_2fa = True
        user.save()
        messages.success(request,'You Enabled the 2FA')
        return redirect('account:account')





def search_user_transactions(request):
    query = None
    transaction_results = []
    if request.method == 'POST':
        my_account = request.user

        query = request.POST.get('search_user_transactions')
        print(f"this is the query = {query}")

        related_users = User.objects.filter(
            Q(username__icontains=query) | Q(kyc__full_name__icontains=query)
        )

        transaction_results = Transaction.objects.filter(
            Q(sender=my_account, reciever__in=related_users) | Q(reciever=my_account, sender__in=related_users)
        ).order_by('-id')

    transaction_results_count = transaction_results.count()
    print(f"this is the transaction_results = {transaction_results}")

    context = {
        'transaction_results': transaction_results,
        'query': query,
        'transaction_results_count': transaction_results_count,
        'my_account': my_account
    }
    return render(request, 'account/search_user_transactions.html', context)




def recipients(request):
    user_transactions = Transaction.objects.filter(Q(sender=request.user) | Q(reciever=request.user))

    recipients = {}
    for transaction in user_transactions:
        if transaction.sender != request.user:
            if transaction.sender not in recipients:
                recipients[transaction.sender] = 1
            else:
                recipients[transaction.sender] += 1

        if transaction.reciever != request.user:
            if transaction.reciever not in recipients:
                recipients[transaction.reciever] = 1
            else:
                recipients[transaction.reciever] += 1
    
    recipient_counts = {}
    for recipient in recipients:
        recipient_count = Transaction.objects.filter(Q(sender=request.user, reciever=recipient) | Q(sender=recipient, reciever=request.user)).count()
        recipient_counts[recipient] = recipient_count

    print(f"recipients: {recipients}")
    print(f"recipient_counts: {recipient_counts}")

    context = {
        'recipients': recipients,
        'recipient_counts': recipient_counts
    }

    return render(request, 'account/recipients.html', context)



def recipient_transactions(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    user = request.user
    transactions = Transaction.objects.filter(Q(sender=user, reciever=recipient) | Q(sender=recipient, reciever=user)).order_by('-id')

    transactions_count = transactions.count()

    context = {
        'transactions': transactions,
        'recipient': recipient,
        'user': user,
        'transactions_count':transactions_count
    }
    return render(request, 'account/recipient_transactions.html', context)


