from core.models import Transaction
from account.models import Account,KYC
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect


def forex_calculate(request):
    return render(request,'forex/sent/forex_calculate.html')



def forex_account_detail_search(request):
    if request.method == 'POST':
        original_currency_amount = request.POST.get('original_currency_amount')
        exchange_rate_input = request.POST.get('exchange_rate_input')
        conversion_fee_input = request.POST.get('conversion_fee_input')
        money_after_fee_input = request.POST.get('money_after_fee_input')
        easypay_rate_input = request.POST.get('easypay_rate_input')
        recipient_gets_amount_input = request.POST.get('recipient_gets_amount_input')
        to_currency = request.POST.get('to_currency')
        from_currency = request.POST.get('from_currency')


        context = {
            'original_currency_amount': original_currency_amount,
            'exchange_rate_input': exchange_rate_input,
            'conversion_fee_input': conversion_fee_input,
            'money_after_fee_input': money_after_fee_input,
            'easypay_rate_input': easypay_rate_input,
            'recipient_gets_amount_input': recipient_gets_amount_input,
            'to_currency':to_currency,
            'from_currency':from_currency
        }


    return render(request,'forex/sent/forex_account_detail_search.html',context)