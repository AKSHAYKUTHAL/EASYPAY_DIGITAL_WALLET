from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Notification,History,DebitCard,ForexDebitCard
from account.models import Account,AccountForex
import datetime
from core.forms import DebitCardForm



def forex_debit_card_detail(request,debit_card_id):
    account = AccountForex.objects.get(user=request.user)
    debit_card = ForexDebitCard.objects.get(debit_card_id=debit_card_id,user=request.user)

    context = {
        'account':account,
        'debit_card':debit_card
    }

    return render(request,'forex/debit_card/forex_debit_card_detail.html',context)





def deactivate_debit_card(request,debit_card_id):
    debit_card = ForexDebitCard.objects.get(debit_card_id=debit_card_id, user=request.user)
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
                return redirect("account:forex_debit_card_detail", debit_card.debit_card_id)

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

                messages.success(request,'Forex Debit Card Activated ')
                return redirect("account:forex_debit_card_detail", debit_card.debit_card_id)
        else:
            messages.error(request,'Incorrect Pin ')
            return redirect("core:debit_card_detail", debit_card.debit_card_id)
        



def delete_debit_card(request, debit_card_id):
    debit_card = ForexDebitCard.objects.get(debit_card_id=debit_card_id, user=request.user)
    user_account = AccountForex.objects.get(user=request.user)
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
            return redirect("account:forex_dashboard")
    else:
        messages.error(request, "Incorrect Pin")
        return redirect("account:forex_debit_card_detail", debit_card.debit_card_id)