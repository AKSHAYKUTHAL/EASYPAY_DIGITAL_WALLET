from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Notification,History,DebitCard
from account.models import Account
import datetime
from core.forms import DebitCardForm


def add_debit_card(request):

    account = Account.objects.get(user=request.user)
    debit_card = DebitCard.objects.filter(user=request.user).order_by('-id')

    month = datetime.datetime.now().month
    year = datetime.datetime.now().year + 5


    if request.method == 'POST':
        if account.debit_card_count < 1:
            form = DebitCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.name = request.user.kyc.full_name
                new_form.amount = account.account_balance
                # new_form.amount = request.user.account.account_balance
                new_form.save()

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
                account.debit_card_count += 1
                account.save()
                messages.success(request,'Debit Card Added Successfully.')
                return redirect('account:dashboard')
        else:
            messages.error(request,'You can only have 1 debit cards at a time')
            return redirect('account:dashboard')
    




def debit_card_detail(request,debit_card_id):
    account = Account.objects.get(user=request.user)
    debit_card = DebitCard.objects.get(debit_card_id=debit_card_id,user=request.user)

    context = {
        'account':account,
        'debit_card':debit_card
    }

    return render(request,'debit_card/debit_card_detail.html',context)



def deactivate_debit_card(request,debit_card_id):
    debit_card = DebitCard.objects.get(debit_card_id=debit_card_id, user=request.user)
    account = request.user.account

    if request.method == 'POST':
        card_pin_number = request.POST.get('card_pin_number')

        if card_pin_number == debit_card.card_pin_number:
            if debit_card.card_status == True:
                debit_card.card_status = False
                debit_card.save()

                Notification.objects.create(
                    user=request.user,
                    notification_type="De-Activated Debit Card",
                    card_number = debit_card.format_card_number(),
                    card_type = debit_card.card_type,
                    card_tier = debit_card.card_tier
                )
                History.objects.create(
                    user=request.user,
                    history_type="De-Activated Debit Card",
                    card_number = debit_card.format_card_number(),
                    card_type = debit_card.card_type,
                    card_tier = debit_card.card_tier
                )
                messages.success(request,'Debit Card De-Activated ')
                return redirect("core:debit_card_detail", debit_card.debit_card_id)

            else:
                debit_card.card_status = True
                debit_card.save()

                Notification.objects.create(
                    user=request.user,
                    notification_type="Activated Debit Card",
                    card_number = debit_card.format_card_number(),
                    card_type = debit_card.card_type,
                    card_tier = debit_card.card_tier
                )
                History.objects.create(
                    user=request.user,
                    history_type="Activated Debit Card",
                    card_number = debit_card.format_card_number(),
                    card_type = debit_card.card_type,
                    card_tier = debit_card.card_tier
                )

                messages.success(request,'Debit Card Activated ')
                return redirect("core:debit_card_detail", debit_card.debit_card_id)
        else:
            messages.error(request,'Incorrect Pin ')
            return redirect("core:debit_card_detail", debit_card.debit_card_id)
        



def delete_debit_card(request, debit_card_id):
    debit_card = DebitCard.objects.get(debit_card_id=debit_card_id, user=request.user)
    user_account = Account.objects.get(user=request.user)
    account = request.user.account
    
    if request.method == 'POST':
        card_pin_number = request.POST.get('card_pin_number')

        if card_pin_number == debit_card.card_pin_number:
            user_account.debit_card_count -= 1
            user_account.save()
            debit_card.delete()

            Notification.objects.create(
                user=request.user,
                notification_type="Deleted Debit Card",
                card_number = debit_card.format_card_number(),
                card_type = debit_card.card_type,
                card_tier = debit_card.card_tier
            )
            History.objects.create(
                user=request.user,
                history_type="Deleted Debit Card",
                card_number = debit_card.format_card_number(),
                card_type = debit_card.card_type,
                card_tier = debit_card.card_tier
            )
            messages.success(request, "Debit Card Deleted Successfull")
            return redirect("account:dashboard")
    else:
        messages.error(request, "Incorrect Pin")
        return redirect("core:debit_card_detail", debit_card.debit_card_id)