from django.shortcuts import render, redirect
from account.models import KYC, Account,AccountForex
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CreditCardForm
from core.models import CreditCard,Notification,History,DebitCard,TransactionForex,ForexDebitCard
from account.forms import AccountForexForm
import datetime
from django.contrib.auth import logout
from decimal import Decimal



def forex_withdraw_check_rate(request):
    user = request.user
    
    account_forex = AccountForex.objects.get(user=user)
 
    sender_account = Account.objects.get(user=user)

    if request.method == 'POST':
        original_currency_amount = request.POST.get('original_currency_amount')
        exchange_rate_input = request.POST.get('exchange_rate_input')
        conversion_fee_input = request.POST.get('conversion_fee_input')
        amount_after_fee_input = request.POST.get('money_after_fee_input')
        easypay_rate_input = request.POST.get('easypay_rate_input')
        recipient_gets_amount_input = request.POST.get('recipient_gets_amount_input')
        to_currency = request.POST.get('to_currency')
        from_currency = request.POST.get('from_currency')

        if account_forex.account_balance >= Decimal(original_currency_amount) :
            new_transaction = TransactionForex.objects.create(
                user = user,
                reciever = user,
                sender = user,
                sender_account = sender_account,
                receiver_account = account_forex,
                reciever_account_currency = to_currency,
                sender_account_currency = from_currency,
                transaction_status = 'Withdraw Processing',
                transaction_type = 'forex',

                original_currency_amount = original_currency_amount,
                exchange_rate = exchange_rate_input,
                conversion_fee = conversion_fee_input,
                amount_after_fee = amount_after_fee_input,
                easypay_rate = easypay_rate_input,
                recipient_gets = recipient_gets_amount_input,
            )
            new_transaction.save()

            transaction_id = new_transaction.transaction_id
            return redirect('account:forex_withdraw_confirm',transaction_id)
        else:
            messages.error(request,'Insufficient balance')
            return redirect('account:forex_withdraw_check_rate')
    
    context = {
        'sender_account':account_forex
    }
    
    return render(request,'forex/withdraw/forex_withdraw_check_rate.html',context)




def forex_withdraw_confirm(request,transaction_id):
    transaction_forex = TransactionForex.objects.get(transaction_id=transaction_id)

    context = {
        'transaction_forex':transaction_forex,
    }

    return render(request,'forex/withdraw/forex_withdraw_confirm.html',context)




def forex_withdraw_confirm_process(request,transaction_id):
    transaction_forex = TransactionForex.objects.get(transaction_id=transaction_id)
    sender_account = transaction_forex.sender_account

    receiver_account = transaction_forex.receiver_account

    sender_account_pin_number = receiver_account.pin_number

    # print(f"sender_account_pin_number = {sender_account_pin_number}")
    try:
        sender_debit_card = ForexDebitCard.objects.get(user=request.user)
    except:
        sender_debit_card = None
    
    try:
        receiver_debit_card = DebitCard.objects.get(user=request.user)
    except:
        receiver_debit_card = None

    if request.method == 'POST':
        if transaction_forex.transaction_status != 'Withdraw Completed':

            pin_number = request.POST.get('pin_number')

            if pin_number == sender_account_pin_number:
                transaction_forex.transaction_status = "Withdraw Completed"
                transaction_forex.save()

                # remove the money
                receiver_account.account_balance -= transaction_forex.original_currency_amount
                receiver_account.save()

                if sender_debit_card is not None:
                    sender_debit_card.amount -= transaction_forex.original_currency_amount
                    sender_debit_card.save()

                # if sender_debit_card is not None:
                #     sender_debit_card.amount -= transaction.amount
                #     sender_debit_card.save()

                # add the monney to the reciever after the fee
                sender_account.account_balance +=  Decimal(transaction_forex.recipient_gets)
                sender_account.save()

                if receiver_debit_card is not None:
                    receiver_debit_card.amount += Decimal(transaction_forex.recipient_gets)
                    receiver_debit_card.save()

                Notification.objects.create(
                    amount=transaction_forex.original_currency_amount,
                    user=sender_account.user,
                    notification_type="Withdraw Completed",
                    forex_sender_account_number = receiver_account.account_number,
                    forex_reciever_account_number = sender_account.account_number,
                    transaction_id = transaction_forex.transaction_id
                )
                History.objects.create(
                    amount=transaction_forex.original_currency_amount,
                    user=sender_account.user,
                    history_type="Withdraw Completed",
                    forex_sender_account_number = receiver_account.account_number,
                    forex_reciever_account_number = sender_account.account_number,
                    transaction_id = transaction_forex.transaction_id
                )

                messages.success(request,'Withdarw Successful')
                return redirect('account:forex_dashboard')
            else:
                messages.error(request,'Incorrect Pin.')
                return redirect('account:forex_withdraw_confirm',transaction_forex.transaction_id)
        else:
            messages.error(request,'You already completed this transaction')
            return redirect('account:forex_dashboard')
    else:
        messages.error(request,'An Error Occcured, Try Again Later.')
        return redirect('account:forex_dashboard')


def forex_withdraw_completed(request,transaction_id):
    transaction = TransactionForex.objects.get(transaction_id=transaction_id)

    context = {
        'transaction':transaction
    }

    return render(request,'forex/withdraw/forex_withdraw_completed.html',context)