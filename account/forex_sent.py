from core.models import Transaction,TransactionForex
from account.models import Account,KYC
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect


def forex_sent_check_rate(request):
    user = request.user

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

        if len(ifsc_swift_code) == 9:
            ifsc_code = ifsc_swift_code
        elif len(ifsc_swift_code) == 11:
            swift_code = ifsc_swift_code
        else:
            messages.error(request,'Please enter a valid IFSC/SWIFT code')

        transaction.full_name = full_name
        transaction.acc
        
    
    context = {
        'transaction':transaction
    }


    return render(request,'forex/sent/forex_account_detail_input.html',context)