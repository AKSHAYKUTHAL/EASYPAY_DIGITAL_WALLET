from core.models import Transaction,TransactionForex,ForexDebitCard,DebitCard
from account.models import Account,KYC,AccountForex
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
import time
from decimal import Decimal


def forex_sent_check_rate(request):
    user = request.user
    account = Account.objects.get(user=user)
    account_forex = AccountForex.objects.get(user=user)

    try:
        if request.method == 'POST':
            original_currency_amount = request.POST.get('original_currency_amount')
            exchange_rate_input = request.POST.get('exchange_rate_input')
            conversion_fee_input = request.POST.get('conversion_fee_input')
            amount_after_fee_input = request.POST.get('money_after_fee_input')
            easypay_rate_input = request.POST.get('easypay_rate_input')
            recipient_gets_amount_input = request.POST.get('recipient_gets_amount_input')
            to_currency = request.POST.get('to_currency')
            from_currency = request.POST.get('from_currency')

            if from_currency == 'INR':
                sender_account = account,
            elif from_currency == 'USD':
                sender_account = account_forex

            new_transaction = TransactionForex.objects.create(
                user = user,
                sender_account_currency = from_currency,
                reciever_account_currency = to_currency,
                transaction_status = 'Forex Sent Processing',
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

            return redirect('account:forex_account_detail_input',transaction_id)
    except:
        messages.error(request,'An Error Occured. Try Again')
        return redirect('account:forex_sent_check_rate')
    

    return render(request,'forex/sent/forex_sent_check_rate.html')




def forex_account_detail_input(request,transaction_id):

    transaction = TransactionForex.objects.get(transaction_id = transaction_id)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        account_number = request.POST.get('account_number')
        ifsc_swift_code = request.POST.get('ifsc_swift_code')
        description = request.POST.get('description')

        if len(ifsc_swift_code) == 9:
            ifsc_code = ifsc_swift_code
            transaction.ifsc_code = ifsc_code
            transaction.save()

        elif len(ifsc_swift_code) == 11:
            swift_code = ifsc_swift_code
            transaction.swift_code = swift_code
            transaction.save()

        else:
            messages.error(request,'Please enter a valid IFSC/SWIFT code')
            return redirect('account:forex_account_detail_input')

        transaction.full_name = full_name
        transaction.account_number = account_number
        transaction.description = description
        transaction.save()
        
        return redirect('account:forex_sent_confirm',transaction_id)
    
    context = {
        'transaction':transaction
    }

    return render(request,'forex/sent/forex_account_detail_input.html',context)


def forex_sent_confirm(request,transaction_id):
    user = request.user
    account_forex = AccountForex.objects.get(user=user)
    account = Account.objects.get(user=user)
    transaction = TransactionForex.objects.get(transaction_id=transaction_id)

    context = {
        'transaction':transaction,
        'user':user,
        'account_forex':account_forex,
        'account':account
    }

    return render(request,'forex/sent/forex_sent_confirm.html',context)






def forex_sent_confirm_process (request,transaction_id):
    user = request.user
    account_forex = AccountForex.objects.get(user=user)
    account = Account.objects.get(user=user)
    transaction = TransactionForex.objects.get(transaction_id=transaction_id)
    

    if request.method == 'POST':
        pin_number = request.POST.get('pin_number')

        if transaction.transaction_status != 'Forex Sent Completed' and transaction.transaction_status != 'Forex Sent Waiting' and transaction.transaction_status != 'Forex Sent Failed' :

            if transaction.sender_account_currency == 'INR':
                sender_account = account
                user_pin_number = sender_account.pin_number

                if sender_account.debit_card_count > 0:
                    try:
                        sender_debit_card = DebitCard.objects.get(user=user)
                    except:
                        sender_debit_card = None
            elif transaction.sender_account_currency == 'USD':
                sender_account = account_forex
                user_pin_number = sender_account.pin_number


                if sender_account.debit_card_count > 0:
                    try:
                        sender_debit_card = ForexDebitCard.objects.get(user=user)
                    except:
                        sender_debit_card = None
   

            if pin_number == user_pin_number:
                transaction.transaction_status = 'Forex Sent Waiting'
                transaction.save()

                sender_account.account_balance -= transaction.original_currency_amount
                sender_account.save()

                if sender_debit_card is not None:
                    sender_debit_card.amount -= transaction.original_currency_amount
                    sender_debit_card.save()

                messages.success(request,'Transfer Initiated')
                return redirect('account:forex_sent_confirm_loader',transaction.transaction_id)
            else:
                messages.error(request,'Incorrect Pin.')
                return redirect('account:forex_sent_confirm',transaction.transaction_id)
        else:
            messages.error(request,'You already Proceesed with this transaction.')
            return redirect('account:forex_dashboard')
               




def forex_sent_confirm_loader(request,transaction_id):
    user = request.user
    transaction = TransactionForex.objects.get(transaction_id=transaction_id)


    if transaction.sender_account_currency == 'INR':
        sender_account = Account.objects.get(user=user)
        if sender_account.debit_card_count > 0:
            try:
                sender_debit_card = DebitCard.objects.get(user=user)
            except:
                sender_debit_card = None
    if transaction.sender_account_currency == 'USD':
        sender_account = AccountForex.objects.get(user=user)
        if sender_account.debit_card_count > 0:
            try:
                sender_debit_card = ForexDebitCard.objects.get(user=user)
            except:
                sender_debit_card = None 

    if transaction.reciever_account_currency == 'INR':
        reciever_account = Account.objects.get(account_number=transaction.account_number)
        if reciever_account.debit_card_count > 0:
            try:
                reciever_debit_card = DebitCard.objects.get(user=reciever_account.user)
            except:
                reciever_debit_card = None
    if transaction.reciever_account_currency == 'USD':
        reciever_account = AccountForex.objects.get(account_number=transaction.account_number)
        if reciever_account.debit_card_count > 0:
            try:
                reciever_debit_card = ForexDebitCard.objects.get(user=reciever_account.user)
            except:
                reciever_debit_card = None 

    print(f"reciever_debit_card = {reciever_debit_card}")



    
    if transaction.reciever_account_currency == 'INR':
        recipient_account_number = transaction.account_number
        recipient_account = Account.objects.get(account_number = recipient_account_number)
        print(f"recipient_account = {recipient_account}")

        if recipient_account is not None:

            if transaction.ifsc_code != 'None':
                if transaction.ifsc_code == recipient_account.ifsc_code :
                    transaction.transaction_status = 'Forex Sent Completed'
                    transaction.save()

                    recipient_account.account_balance += Decimal(transaction.recipient_gets)
                    recipient_account.save()

                    if reciever_debit_card is not None:
                        reciever_debit_card.amount += Decimal(transaction.recipient_gets)
                        reciever_debit_card.save()
                    
                    
                    messages.success(request,'The Money is Sent')
                    return redirect('account:forex_sent_completed',transaction_id)
                
                else:
                    transaction.transaction_status = 'Forex Sent Failed'
                    transaction.save()

                    sender_account.account_balance += Decimal(transaction.original_currency_amount)
                    sender_account.save()

                    sender_debit_card.amount += Decimal(transaction.original_currency_amount)
                    sender_debit_card.save()

                    
                    messages.error(request,'Not a valid IFSC code. Transaction Failed. Your Money is Returned')
                    return redirect('account:forex_dashboard')



            elif transaction.swift_code != 'None':
                if transaction.swift_code == recipient_account.swift_code :
                    transaction.transaction_status = 'Forex Sent Completed'
                    transaction.save()

                    recipient_account.account_balance += Decimal(transaction.recipient_gets)
                    recipient_account.save()

                    if reciever_debit_card is not None:
                        reciever_debit_card.amount += Decimal(transaction.recipient_gets)
                        reciever_debit_card.save()

                    messages.success(request,'The Money is Sent')
                    return redirect('account:forex_sent_completed',transaction_id)
                
                else:
                    transaction.transaction_status = 'Forex Sent Failed'
                    transaction.save()

                    sender_account.account_balance += Decimal(transaction.original_currency_amount)
                    sender_account.save()

                    sender_debit_card.amount += Decimal(transaction.original_currency_amount)
                    sender_debit_card.save()
    
                    messages.error(request,'Not a valid Swift code. Transaction Failed. Your Money is Returned.')
                    return redirect('account:forex_dashboard')
                
        else:
            transaction.transaction_status = 'Forex Sent Failed'
            transaction.save()

            sender_account.account_balance += Decimal(transaction.original_currency_amount)
            sender_account.save()

            sender_debit_card.amount += Decimal(transaction.original_currency_amount)
            sender_debit_card.save()

            messages.error(request,'Not a valid Account Number. Transaction Failed. Your Money is Returned.')
            return redirect('account:forex_dashboard')
    else:
        if transaction.reciever_account_currency == 'USD':
            recipient_account_number = transaction.account_number
            recipient_account = AccountForex.objects.get(account_number = recipient_account_number)

            if recipient_account is not None:
                
                if transaction.ifsc_code != 'None':
                    if transaction.ifsc_code == recipient_account.ifsc_code :
                        transaction.transaction_status = 'Forex Sent Completed'
                        transaction.save()

                        recipient_account.account_balance += Decimal(transaction.recipient_gets)
                        recipient_account.save()

                        if reciever_debit_card is not None:
                            reciever_debit_card.amount += Decimal(transaction.recipient_gets)
                            reciever_debit_card.save()
                        
                        messages.success(request,'The Money is Sent')
                        return redirect('account:forex_sent_completed',transaction_id)
                    
                    else:
                        transaction.transaction_status = 'Forex Sent Failed'
                        transaction.save()

                        sender_account.account_balance += Decimal(transaction.original_currency_amount)
                        sender_account.save()

                        sender_debit_card.amount += Decimal(transaction.original_currency_amount)
                        sender_debit_card.save()

                        messages.error(request,'Not a valid IFSC code. Transaction Failed. Your Money is Returned')
                        return redirect('account:forex_dashboard')



                elif transaction.swift_code != 'None':
                    if transaction.swift_code == recipient_account.swift_code :
                        transaction.transaction_status = 'Forex Sent Completed'
                        transaction.save()

                        recipient_account.account_balance += Decimal(transaction.recipient_gets)
                        recipient_account.save()

                        if reciever_debit_card is not None:
                            reciever_debit_card.amount += Decimal(transaction.recipient_gets)
                            reciever_debit_card.save()

                        messages.success(request,'The Money is Sent')
                        return redirect('account:forex_sent_completed',transaction_id)
                    
                    else:
                        transaction.transaction_status = 'Forex Sent Failed'
                        transaction.save()

                        sender_account.account_balance += Decimal(transaction.original_currency_amount)
                        sender_account.save()

                        sender_debit_card.amount += Decimal(transaction.original_currency_amount)
                        sender_debit_card.save()

                        messages.error(request,'Not a valid Swift code. Transaction Failed. Your Money is Returned.')
                        return redirect('account:forex_dashboard')
                    
            else:
                transaction.transaction_status = 'Forex Sent Failed'
                transaction.save()

                sender_account.account_balance += Decimal(transaction.original_currency_amount)
                sender_account.save()

                sender_debit_card.amount += Decimal(transaction.original_currency_amount)
                sender_debit_card.save()
                

                messages.error(request,'Not a valid Account Number. Transaction Failed. Your Money is Returned.')
                return redirect('account:forex_dashboard')
            
    


def forex_sent_completed(request,transaction_id):
    user = request.user
    transaction = TransactionForex.objects.get(transaction_id=transaction_id)

    if transaction.sender_account_currency == 'INR':
        from_account = Account.objects.get(user=user)
    if transaction.sender_account_currency == 'USD':
        from_account = AccountForex.objects.get(user=user)
    

    if transaction.reciever_account_currency == 'INR':
        to_account = Account.objects.get(user=user)
    if transaction.reciever_account_currency == 'USD':
        to_account = AccountForex.objects.get(user=user)


    context = {
        'transaction':transaction,
        'from_account':from_account,
        'to_account':to_account
    }
    return render(request,'forex/sent/forex_sent_completed.html',context)