from django.shortcuts import render, redirect
from account.models import KYC, Account,AccountForeign
from account.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CreditCardForm
from core.models import CreditCard,Notification,History,DebitCard
from account.forms import AccountForeignForm
import datetime
from django.contrib.auth import logout



def foreign_account_add(request):
    user = request.user
    account = Account.objects.get(user=user)

    form = AccountForeignForm(request.POST)


    context = {
        'account':account,
        'form':form
    }

    return render(request,'foreign/foreign_account_add.html',context)


def foreign_account_create(request):
    user = request.user
    account = Account.objects.get(user=user)

    if request.method == 'POST':
        form = AccountForeignForm(request.POST)

        try:
            account_foreign = AccountForeign.objects.get(user=request.user)
            messages.error(request,'You already have a forex account')

        except AccountForeign.DoesNotExist:
            pin_number = request.POST.get('pin_number')

            if pin_number == user.account.pin_number:
                if form.is_valid():
                    new_form = form.save(commit=False)
                    new_form.user = request.user
                    new_form.save()
                messages.success(request,'You created a Forex Account')
                return redirect('account:foreign_dashboard',)
            else:
                messages.error(request,'Incorrect Pin')
                return redirect('account:foreign_account_add')
        
    else:
        form = AccountForeignForm()




def foreign_dashboard(request):
    user = request.user
    kyc = KYC.objects.get(user=user)
    try:
        account_foreign = AccountForeign.objects.get(user=user)



    except AccountForeign.DoesNotExist:
        messages.error(request,'You dont have a Forex account,Please create one, then proceed')
        return redirect('account:foreign_account_add')
    

    context = {
        'account_foreign':account_foreign,
        'user':user,
        'kyc':kyc
    }

    return render(request,'foreign/foreign_dashboard.html',context)


def foreign_deposit_check_rate(request):
    return render(request,'foreign/deposit/foreign_deposit_check_rate.html')