from django.shortcuts import render, redirect
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from core.models import Transaction,Notification,CreditCard,History
import time
from decimal import Decimal


def crypto(request):
    return render(request,'crypto/crypto_chart.html')