from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import CreditCard,Notification,History,DebitCard
from account.models import Account
import datetime
from decimal import Decimal
from account.models import KYC
from itertools import chain


def all_cards(request):
    try:
        kyc = KYC.objects.get(user=request.user)
    except:
        messages.error(request,'You need to submit your KYC!')
        return redirect('account:kyc_reg')
    
    account = Account.objects.get(user=request.user)
    all_card =chain(
        CreditCard.objects.filter(user=request.user).order_by('-id'),
        DebitCard.objects.filter(user=request.user)
    ) 
    all_card_list = list(all_card)

    context = {
        "account":account,
        "all_card_list":all_card_list,
    }
    return render(request, "credit_card/all_cards.html", context)



def credit_card_detail(request,credit_card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(credit_card_id=credit_card_id,user=request.user)

    context = {
        'account':account,
        'credit_card':credit_card
    }

    return render(request,'credit_card/credit_card_detail.html',context)


def fund_credit_card(request, credit_card_id):
    credit_card = CreditCard.objects.get(credit_card_id=credit_card_id, user=request.user,card_status=True)
    account = request.user.account
    try:
        debit_card = DebitCard.objects.get(user=request.user)
    except:
        debit_card = None

    
    if request.method == "POST":
        funding_amount = request.POST.get("funding_amount") # 25
        fund_transfer_pin_number = request.POST.get('fund_transfer_pin_number')
        account = Account.objects.get(user=request.user)

        if funding_amount:
            if Decimal(funding_amount) <= account.account_balance:
                if fund_transfer_pin_number == account.pin_number:
                    account.account_balance -= Decimal(funding_amount) ## 14,790.00 - 20
                    account.save()
                    if debit_card is not None:
                        debit_card.amount -= Decimal(funding_amount)
                        debit_card.save()

                    credit_card.amount += Decimal(funding_amount)
                    credit_card.save()
                    
                    Notification.objects.create(
                        amount  = funding_amount,
                        user = request.user,
                        notification_type = "Funded Credit Card",
                        card_number = credit_card.format_card_number(),
                        card_type = credit_card.card_type,
                        card_tier = credit_card.card_tier
                    )
                    History.objects.create(
                        amount  = funding_amount,
                        user = request.user,
                        history_type = "Funded Credit Card",
                        card_number = credit_card.format_card_number(),
                        card_type = credit_card.card_type,
                        card_tier = credit_card.card_tier
                    )
                    
                    messages.success(request, "Funding Successfull")
                    return redirect("core:credit_card_detail", credit_card.credit_card_id)
                
                else:
                    messages.error(request,'Incorrect Pin Number.')
                    return redirect("core:credit_card_detail", credit_card.credit_card_id)
            else:
                messages.error(request, "Insufficient Funds")
                return redirect("core:credit_card_detail", credit_card.credit_card_id)
        else:
                messages.error(request, "Type a valid amount to send")
                return redirect("core:credit_card_detail", credit_card.credit_card_id)
        
        


def withdraw_fund_from_credit_card(request, credit_card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(credit_card_id=credit_card_id, user=request.user,card_status=True)

    try:
        debit_card = DebitCard.objects.get(user=request.user)
    except:
        debit_card = None

    if request.method == "POST":
        withdraw_amount = request.POST.get("withdraw_amount")
        card_pin_number = request.POST.get("card_pin_number")
            
        try:
            if credit_card.amount >= Decimal(withdraw_amount) and credit_card.amount != 0.00:
                if card_pin_number == credit_card.card_pin_number:

                    account.account_balance += Decimal(withdraw_amount)
                    account.save()

                    if debit_card is not None:
                        debit_card.amount += Decimal(withdraw_amount)
                        debit_card.save()


                    credit_card.amount -= Decimal(withdraw_amount)
                    credit_card.save()
                
                    Notification.objects.create(
                        user=request.user,
                        amount=withdraw_amount,
                        notification_type="Withdrew Credit Card Funds",
                        card_number = credit_card.format_card_number(),
                        card_type = credit_card.card_type,
                        card_tier = credit_card.card_tier
                    )
                    History.objects.create(
                        user=request.user,
                        amount=withdraw_amount,
                        history_type="Withdrew Credit Card Funds",
                        card_number = credit_card.format_card_number(),
                        card_type = credit_card.card_type,
                        card_tier = credit_card.card_tier
                    )

                    messages.success(request, "Withdrawal Successfull")
                    return redirect("core:credit_card_detail", credit_card.credit_card_id)
                else:
                    messages.error(request, "Incorrect Pin Number")
                    return redirect("core:credit_card_detail", credit_card.credit_card_id)
            elif credit_card.amount == 0.00:
                messages.error(request, "Insufficient Funds")
                return redirect("core:credit_card_detail", credit_card.credit_card_id)
            else:
                messages.error(request, "Insufficient Funds")
                return redirect("core:credit_card_detail", credit_card.credit_card_id)
        except:
            messages.error(request, "Please Enter a valid amount")
            return redirect("core:credit_card_detail", credit_card.credit_card_id)
        




def delete_credit_card(request, credit_card_id):
    credit_card = CreditCard.objects.get(credit_card_id=credit_card_id, user=request.user)
    user_account = Account.objects.get(user=request.user)
    account = request.user.account

    try:
        debit_card = DebitCard.objects.get(user=request.user)
    except:
        debit_card = None
    
    if request.method == 'POST':
        card_pin_number = request.POST.get('card_pin_number')

        if card_pin_number == credit_card.card_pin_number:
            if credit_card.amount > 0:
                account.account_balance += credit_card.amount
                account.save()
                
                if debit_card is not None:
                    debit_card.amount += credit_card.amount
                    debit_card.save()
                    
                credit_card.delete()

                Notification.objects.create(
                    user=request.user,
                    notification_type="Deleted Credit Card",
                    card_number = credit_card.format_card_number(),
                    card_type = credit_card.card_type,
                    card_tier = credit_card.card_tier
                )
                History.objects.create(
                    user=request.user,
                    history_type="Deleted Credit Card",
                    card_number = credit_card.format_card_number(),
                    card_type = credit_card.card_type,
                    card_tier = credit_card.card_tier
                )

                messages.success(request, "Credit Card Deleted Successfull")
                return redirect("account:dashboard")
            else:
                credit_card.delete()

                Notification.objects.create(
                    user=request.user,
                    notification_type="Deleted Credit Card",
                    card_number = credit_card.format_card_number(),
                    card_type = credit_card.card_type,
                    card_tier = credit_card.card_tier
                )
                History.objects.create(
                    user=request.user,
                    history_type="Deleted Credit Card",
                    card_number = credit_card.format_card_number(),
                    card_type = credit_card.card_type,
                    card_tier = credit_card.card_tier
                )
                user_account.credit_card_count -= 1
                user_account.save()
                messages.success(request, "Credit Card Deleted Successfull")
                return redirect("account:dashboard")
        else:
            messages.error(request, "Incorrect Pin")
            return redirect("core:credit_card_detail", credit_card.credit_card_id)



def deactivate_credit_card(request,credit_card_id):
    credit_card = CreditCard.objects.get(credit_card_id=credit_card_id, user=request.user)
    account = request.user.account

    if request.method == 'POST':
        card_pin_number = request.POST.get('card_pin_number')

        if card_pin_number == credit_card.card_pin_number:
            if credit_card.card_status == True:
                credit_card.card_status = False
                credit_card.save()

                Notification.objects.create(
                    user=request.user,
                    notification_type="De-Activated Credit Card",
                    card_number = credit_card.format_card_number(),
                    card_type = credit_card.card_type,
                    card_tier = credit_card.card_tier
                )
                History.objects.create(
                    user=request.user,
                    history_type="De-Activated Credit Card",
                    card_number = credit_card.format_card_number(),
                    card_type = credit_card.card_type,
                    card_tier = credit_card.card_tier
                )
                messages.success(request,'Credit Card De-Activated ')
                return redirect("core:credit_card_detail", credit_card.credit_card_id)

            else:
                credit_card.card_status = True
                credit_card.save()

                Notification.objects.create(
                    user=request.user,
                    notification_type="Activated Credit Card",
                    card_number = credit_card.format_card_number(),
                    card_type = credit_card.card_type,
                    card_tier = credit_card.card_tier
                )
                History.objects.create(
                    user=request.user,
                    history_type="Activated Credit Card",
                    card_number = credit_card.format_card_number(),
                    card_type = credit_card.card_type,
                    card_tier = credit_card.card_tier
                )

                messages.success(request,'Credit Card Activated ')
                return redirect("core:credit_card_detail", credit_card.credit_card_id)
        else:
            messages.error(request,'Incorrect Pin ')
            return redirect("core:credit_card_detail", credit_card.credit_card_id)



