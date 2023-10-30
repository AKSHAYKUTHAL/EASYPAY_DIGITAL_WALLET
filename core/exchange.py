from core.models import Transaction
from account.models import Account,KYC
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect


def exchange(request):
    return render(request,'exchange/exchange.html')