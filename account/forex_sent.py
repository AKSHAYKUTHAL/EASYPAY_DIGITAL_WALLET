from core.models import Transaction,TransactionForex,ForexDebitCard,DebitCard,History,Notification
from account.models import Account,KYC,AccountForex
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
import time
from decimal import Decimal


def forex_sent_check_rate(request):
    try:
        user = request.user
        account = Account.objects.get(user=user)
        account_forex = AccountForex.objects.get(user=user)

        if request.method == 'POST':
            original_currency_amount = request.POST.get('original_currency_amount')
            exchange_rate_input = request.POST.get('exchange_rate_input')
            conversion_fee_input = request.POST.get('conversion_fee_input')
            amount_after_fee_input = request.POST.get('money_after_fee_input')
            easypay_rate_input = request.POST.get('easypay_rate_input')
            recipient_gets_amount_input = request.POST.get('recipient_gets_amount_input')
            to_currency = request.POST.get('to_currency')
            from_currency = request.POST.get('from_currency')

            if from_currency == to_currency:
                messages.error(request, 'Please choose different currencies')
            elif from_currency == 'INR':
                if account.account_balance > Decimal(original_currency_amount):
                    new_transaction = TransactionForex.objects.create(
                        user=user,
                        sender_account_currency=from_currency,
                        reciever_account_currency=to_currency,
                        transaction_status='None',
                        transaction_type='forex',
                        original_currency_amount=original_currency_amount,
                        exchange_rate=exchange_rate_input,
                        conversion_fee=conversion_fee_input,
                        amount_after_fee=amount_after_fee_input,
                        easypay_rate=easypay_rate_input,
                        recipient_gets=recipient_gets_amount_input,
                    )
                    new_transaction.save()
                    transaction_id = new_transaction.transaction_id

                    return redirect('account:forex_account_detail_input', transaction_id)
                else:
                    messages.error(request, 'Insufficient Balance In your Selected Currency Account')
            elif from_currency == 'USD':
                if account_forex.account_balance > Decimal(original_currency_amount):
                    new_transaction = TransactionForex.objects.create(
                        user=user,
                        sender_account_currency=from_currency,
                        reciever_account_currency=to_currency,
                        transaction_status='None',
                        transaction_type='forex',
                        original_currency_amount=original_currency_amount,
                        exchange_rate=exchange_rate_input,
                        conversion_fee=conversion_fee_input,
                        amount_after_fee=amount_after_fee_input,
                        easypay_rate=easypay_rate_input,
                        recipient_gets=recipient_gets_amount_input,
                    )
                    new_transaction.save()
                    transaction_id = new_transaction.transaction_id

                    return redirect('account:forex_account_detail_input', transaction_id)
                else:
                    messages.error(request, 'Insufficient Balance In your Selected Currency Account')
            else:
                messages.error(request, 'Invalid Currency Type')
        

    except Account.DoesNotExist:
        messages.error(request, 'Account does not exist for the user')
    except AccountForex.DoesNotExist:
        messages.error(request, 'Forex account does not exist for the user')
    except Exception as e:
        messages.error(request, f'An Error Occurred: {str(e)}')

    return render(request, 'forex/sent/forex_sent_check_rate.html')




def forex_account_detail_input(request,transaction_id):
    try:
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
            transaction.transaction_status = 'Forex Sent Processing'
            transaction.save()
            
            return redirect('account:forex_sent_confirm',transaction_id)
    except TransactionForex.DoesNotExist:
        messages.error(request,'Some Error Occured, Please Try Again')
        return redirect('account:forex_sent_check_rate')

    
    context = {
        'transaction':transaction
    }

    return render(request,'forex/sent/forex_account_detail_input.html',context)


def forex_sent_confirm(request,transaction_id):
    try:
        user = request.user
        account_forex = AccountForex.objects.get(user=user)
        account = Account.objects.get(user=user)
        transaction = TransactionForex.objects.get(transaction_id=transaction_id)

        transaction.transaction_status = 'Forex Sent Processing'

        transaction.save()

    except TransactionForex.DoesNotExist:
        messages.error(request,'Some Error Occured, Please Try Again')
        return redirect('account:forex_sent_check_rate')
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
                if sender_account.account_balance > Decimal(transaction.original_currency_amount):
                    transaction.transaction_status = 'Forex Sent Waiting'
                    transaction.save()

                    sender_account.account_balance -= transaction.original_currency_amount
                    sender_account.save()

                    if sender_debit_card is not None:
                        sender_debit_card.amount -= transaction.original_currency_amount
                        sender_debit_card.save()

                    messages.success(request,'Transfer Initiated')
                    return redirect('account:forex_sent_confirmation',transaction.transaction_id)
                else:
                    messages.error(request,'Insufficient Balance')
                    return redirect('account:forex_sent_check_rate')
            else:
                messages.error(request,'Incorrect Pin.')
                return redirect('account:forex_sent_confirm',transaction.transaction_id)
        else:
            messages.error(request,'You already Proceesed with this transaction.')
            return redirect('account:forex_dashboard')
            
               




def forex_sent_confirmation(request,transaction_id):
    user = request.user
    transaction = TransactionForex.objects.get(transaction_id=transaction_id)


    if transaction.sender_account_currency == 'INR':
        sender_account = Account.objects.get(user=user)
        transaction.from_account_number = sender_account.account_number

        if sender_account.debit_card_count > 0:
            try:
                sender_debit_card = DebitCard.objects.get(user=user)
            except:
                sender_debit_card = None
    if transaction.sender_account_currency == 'USD':
        sender_account = AccountForex.objects.get(user=user)
        transaction.from_account_number = sender_account.account_number

        if sender_account.debit_card_count > 0:
            try:
                sender_debit_card = ForexDebitCard.objects.get(user=user)
            except:
                sender_debit_card = None 

    if transaction.reciever_account_currency == 'INR':
        try:
            reciever_account = Account.objects.get(account_number=transaction.account_number)
            if reciever_account.debit_card_count > 0:
                try:
                    reciever_debit_card = DebitCard.objects.get(user=reciever_account.user)
                except:
                    reciever_debit_card = None
        except Account.DoesNotExist:
            reciever_account = None
    if transaction.reciever_account_currency == 'USD':
        try:
            reciever_account = AccountForex.objects.get(account_number=transaction.account_number)
            if reciever_account.debit_card_count > 0:
                try:
                    reciever_debit_card = ForexDebitCard.objects.get(user=reciever_account.user)
                except:
                    reciever_debit_card = None 
        except AccountForex.DoesNotExist:
            reciever_account = None




    
    if transaction.reciever_account_currency == 'INR':
        recipient_account_number = transaction.account_number
        try:
            recipient_account = Account.objects.get(account_number = recipient_account_number)
        except Account.DoesNotExist:
            recipient_account = None

        if recipient_account is not None:
            
            # print(f"transaction.ifsc_code = {transaction.ifsc_code}")
            # print(f"recipient_account.ifsc_code = {recipient_account.ifsc_code}")


            if transaction.ifsc_code != 'None':
                clean_transaction_ifsc_code = transaction.ifsc_code.strip() if transaction.ifsc_code else None
                clean_recipient_ifsc_code = recipient_account.ifsc_code.strip() if recipient_account.ifsc_code else None

                if clean_transaction_ifsc_code == clean_recipient_ifsc_code :
                    transaction.transaction_status = 'Forex Sent Completed'
                    transaction.save()

                    recipient_account.account_balance += Decimal(transaction.recipient_gets)
                    recipient_account.save()

                    if reciever_debit_card is not None:
                        reciever_debit_card.amount += Decimal(transaction.recipient_gets)
                        reciever_debit_card.save()

                    Notification.objects.create(
                        user=request.user,
                        notification_type="Forex Sent Completed",
                        amount = Decimal(transaction.original_currency_amount),
                        transaction_id = transaction_id,
                        forex_sender_account_number = transaction.from_account_number,
                        forex_reciever_account_number = recipient_account_number
                    )
                    History.objects.create(
                        user=request.user,
                        history_type="Forex Sent Completed",
                        amount = Decimal(transaction.original_currency_amount),
                        transaction_id = transaction_id,
                        forex_sender_account_number = transaction.from_account_number,
                        forex_reciever_account_number = recipient_account_number,
                    )
                    
                    
                    return redirect('account:forex_sent_confirm_loader',transaction_id)
                
                else:
                    transaction.transaction_status = 'Forex Sent Failed'
                    transaction.save()

                    sender_account.account_balance += Decimal(transaction.original_currency_amount)
                    sender_account.save()

                    sender_debit_card.amount += Decimal(transaction.original_currency_amount)
                    sender_debit_card.save()

                    Notification.objects.create(
                        user=request.user,
                        notification_type="Forex Sent Failed",
                        amount = Decimal(transaction.original_currency_amount),
                        transaction_id = transaction_id,
                        forex_sender_account_number = transaction.from_account_number,
                        forex_reciever_account_number = recipient_account_number
                    )
                    History.objects.create(
                        user=request.user,
                        history_type="Forex Sent Failed",
                        amount = Decimal(transaction.original_currency_amount),
                        transaction_id = transaction_id,
                        forex_sender_account_number = transaction.from_account_number,
                        forex_reciever_account_number = recipient_account_number,
                    )

                    
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

                    Notification.objects.create(
                        user=request.user,
                        notification_type="Forex Sent Completed",
                        amount = Decimal(transaction.original_currency_amount),
                        transaction_id = transaction_id,
                        forex_sender_account_number = transaction.from_account_number,
                        forex_reciever_account_number = recipient_account_number
                    )
                    History.objects.create(
                        user=request.user,
                        history_type="Forex Sent Completed",
                        amount = Decimal(transaction.original_currency_amount),
                        transaction_id = transaction_id,
                        forex_sender_account_number = transaction.from_account_number,
                        forex_reciever_account_number = recipient_account_number,
                    )

                    return redirect('account:forex_sent_confirm_loader',transaction_id)
                
                else:
                    transaction.transaction_status = 'Forex Sent Failed'
                    transaction.save()

                    sender_account.account_balance += Decimal(transaction.original_currency_amount)
                    sender_account.save()

                    sender_debit_card.amount += Decimal(transaction.original_currency_amount)
                    sender_debit_card.save()

                    Notification.objects.create(
                        user=request.user,
                        notification_type="Forex Sent Failed",
                        amount = Decimal(transaction.original_currency_amount),
                        transaction_id = transaction_id,
                        forex_sender_account_number = transaction.from_account_number,
                        forex_reciever_account_number = recipient_account_number
                    )
                    History.objects.create(
                        user=request.user,
                        history_type="Forex Sent Failed",
                        amount = Decimal(transaction.original_currency_amount),
                        transaction_id = transaction_id,
                        forex_sender_account_number = transaction.from_account_number,
                        forex_reciever_account_number = recipient_account_number,
                    )
    
                    messages.error(request,'Not a valid Swift code. Transaction Failed. Your Money is Returned.')
                    return redirect('account:forex_dashboard')
                
        else:
            transaction.transaction_status = 'Forex Sent Failed'
            transaction.save()

            sender_account.account_balance += Decimal(transaction.original_currency_amount)
            sender_account.save()

            sender_debit_card.amount += Decimal(transaction.original_currency_amount)
            sender_debit_card.save()

            Notification.objects.create(
                user=request.user,
                notification_type="Forex Sent Failed",
                amount = Decimal(transaction.original_currency_amount),
                transaction_id = transaction_id,
                forex_sender_account_number = transaction.from_account_number,
                forex_reciever_account_number = recipient_account_number
            )
            History.objects.create(
                user=request.user,
                history_type="Forex Sent Failed",
                amount = Decimal(transaction.original_currency_amount),
                transaction_id = transaction_id,
                forex_sender_account_number = transaction.from_account_number,
                forex_reciever_account_number = recipient_account_number,
            )

            messages.error(request,'Not a valid Account Number. Transaction Failed. Your Money is Returned.')
            return redirect('account:forex_dashboard')
    else:
        if transaction.reciever_account_currency == 'USD':
            recipient_account_number = transaction.account_number
            try:
                recipient_account = AccountForex.objects.get(account_number = recipient_account_number)
            except:
                recipient_account = None

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

                        Notification.objects.create(
                            user=request.user,
                            notification_type="Forex Sent Completed",
                            amount = Decimal(transaction.original_currency_amount),
                            transaction_id = transaction_id,
                            forex_sender_account_number = transaction.from_account_number,
                            forex_reciever_account_number = recipient_account_number
                        )
                        History.objects.create(
                            user=request.user,
                            history_type="Forex Sent Completed",
                            amount = Decimal(transaction.original_currency_amount),
                            transaction_id = transaction_id,
                            forex_sender_account_number = transaction.from_account_number,
                            forex_reciever_account_number = recipient_account_number,
                        )
                        
                        return redirect('account:forex_sent_confirm_loader',transaction_id)
                    
                    else:
                        transaction.transaction_status = 'Forex Sent Failed'
                        transaction.save()

                        sender_account.account_balance += Decimal(transaction.original_currency_amount)
                        sender_account.save()

                        sender_debit_card.amount += Decimal(transaction.original_currency_amount)
                        sender_debit_card.save()

                        Notification.objects.create(
                            user=request.user,
                            notification_type="Forex Sent Failed",
                            amount = Decimal(transaction.original_currency_amount),
                            transaction_id = transaction_id,
                            forex_sender_account_number = transaction.from_account_number,
                            forex_reciever_account_number = recipient_account_number
                        )
                        History.objects.create(
                            user=request.user,
                            history_type="Forex Sent Failed",
                            amount = Decimal(transaction.original_currency_amount),
                            transaction_id = transaction_id,
                            forex_sender_account_number = transaction.from_account_number,
                            forex_reciever_account_number = recipient_account_number,
                        )

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

                        Notification.objects.create(
                            user=request.user,
                            notification_type="Forex Sent Completed",
                            amount = Decimal(transaction.original_currency_amount),
                            transaction_id = transaction_id,
                            forex_sender_account_number = transaction.from_account_number,
                            forex_reciever_account_number = recipient_account_number
                        )
                        History.objects.create(
                            user=request.user,
                            history_type="Forex Sent Completed",
                            amount = Decimal(transaction.original_currency_amount),
                            transaction_id = transaction_id,
                            forex_sender_account_number = transaction.from_account_number,
                            forex_reciever_account_number = recipient_account_number,
                        )

                        return redirect('account:forex_sent_confirm_loader',transaction_id)
                    
                    else:
                        transaction.transaction_status = 'Forex Sent Failed'
                        transaction.save()

                        sender_account.account_balance += Decimal(transaction.original_currency_amount)
                        sender_account.save()

                        sender_debit_card.amount += Decimal(transaction.original_currency_amount)
                        sender_debit_card.save()

                        Notification.objects.create(
                            user=request.user,
                            notification_type="Forex Sent Failed",
                            amount = Decimal(transaction.original_currency_amount),
                            transaction_id = transaction_id,
                            forex_sender_account_number = transaction.from_account_number,
                            forex_reciever_account_number = recipient_account_number
                        )
                        History.objects.create(
                            user=request.user,
                            history_type="Forex Sent Failed",
                            amount = Decimal(transaction.original_currency_amount),
                            transaction_id = transaction_id,
                            forex_sender_account_number = transaction.from_account_number,
                            forex_reciever_account_number = recipient_account_number,
                        )

                        messages.error(request,'Not a valid Swift code. Transaction Failed. Your Money is Returned.')
                        return redirect('account:forex_dashboard')
                    
            else:
                transaction.transaction_status = 'Forex Sent Failed'
                transaction.save()

                sender_account.account_balance += Decimal(transaction.original_currency_amount)
                sender_account.save()

                sender_debit_card.amount += Decimal(transaction.original_currency_amount)
                sender_debit_card.save()
                

                Notification.objects.create(
                    user=request.user,
                    notification_type="Forex Sent Failed",
                    amount = Decimal(transaction.original_currency_amount),
                    transaction_id = transaction_id,
                    forex_sender_account_number = transaction.from_account_number,
                    forex_reciever_account_number = recipient_account_number
                )
                History.objects.create(
                    user=request.user,
                    history_type="Forex Sent Failed",
                    amount = Decimal(transaction.original_currency_amount),
                    transaction_id = transaction_id,
                    forex_sender_account_number = transaction.from_account_number,
                    forex_reciever_account_number = recipient_account_number,
                )

                messages.error(request,'Not a valid Account Number. Transaction Failed. Your Money is Returned.')
                return redirect('account:forex_dashboard')
            



def forex_sent_confirm_loader(request,transaction_id):
    transaction = TransactionForex.objects.get(transaction_id=transaction_id)

    context = {
        'transaction':transaction,
    }
    return render(request,'forex/sent/forex_sent_confirm_loader.html',context)
            
    


def forex_sent_completed(request,transaction_id):
    user = request.user
    transaction = TransactionForex.objects.get(transaction_id=transaction_id)

    if transaction.transaction_status == 'Forex Sent Completed' and request.META.get('HTTP_REFERER') != 'http://127.0.0.1:8000/account/dashboard/':
        messages.success(request, 'Your Money has been Sent')


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



def forex_sent_detail(request,transaction_id):

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
    return render(request,'forex/sent/forex_sent_detail.html',context)






def delete_forex_transaction(request,transaction_id):
    transaction = TransactionForex.objects.get(transaction_id=transaction_id)
    transaction.delete()

    messages.success(request,'The Forex Transaction deleted succesfully.')
    return redirect('account:forex_dashboard')