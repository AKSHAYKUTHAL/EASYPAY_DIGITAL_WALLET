from django.shortcuts import render, redirect
from account.models import KYC, Account
from account.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CreditCardForm
from core.models import CreditCard,Notification,History,DebitCard
import datetime
from django.contrib.auth import logout
from account.mixins import MessageHandler
from userauths.models import User
import random





def account(request): 
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.error(request,'You need to submit your KYC!')
            return redirect('account:kyc_reg')
        
        account = Account.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user=request.user).order_by('-id')
        debit_card = DebitCard.objects.filter(user=request.user).order_by('-id')


        form = CreditCardForm(request.POST)


        month = datetime.datetime.now().month
        year = datetime.datetime.now().year + 5

        
        if request.method == 'POST':
            if account.credit_card_count < 2:
                form = CreditCardForm(request.POST)
                if form.is_valid():
                    new_form = form.save(commit=False)
                    new_form.user = request.user
                    new_form.name = request.user.kyc.full_name
                    # new_form.amount = request.user.account.account_balance
                    new_form.save()

                    credit_card_id = new_form.credit_card_id

                    Notification.objects.create(
                        user=request.user,
                        notification_type="Added Credit Card",
                        card_number = new_form.format_card_number(),
                        card_type = new_form.card_type,
                        card_tier = new_form.card_tier
                    )
                    History.objects.create(
                        user=request.user,
                        history_type="Added Credit Card",
                        card_number = new_form.format_card_number(),
                        card_type = new_form.card_type,
                        card_tier = new_form.card_tier
                    )
                    account.credit_card_count += 1
                    account.save()
                    messages.success(request,'Card Added Successfully.')
                    return redirect('account:account')
            else:
                messages.error(request,'You can only have 2 credit cards at a time')
                return redirect('account:account')
        else:
            form = CreditCardForm()
        

    else:
        messages.error(request,'You need to login to access the dashboard')
        return redirect('userauths:sign_in')
    context = {
        'kyc':kyc,
        'account':account,
        'credit_card':credit_card,
        'month':month,
        'year':year,
        'form':form,
        'debit_card':debit_card,
    }
    return render(request,'account/account.html',context)



def delete_account(request,id):
    account = Account.objects.get(id=id, user=request.user)
    credit_card = CreditCard.objects.filter(user=request.user)

    credit_card_balance = 0

    if request.method == 'POST':
        pin_number = request.POST.get('pin_number')
        
        try:
            for c in credit_card :
                credit_card_balance += c.amount 
        except:
            credit_card_balance = 0


        if account.account_balance <= 0 and account.deleted_account == False :
            if credit_card_balance == 0:

                if pin_number == account.pin_number:
                    account.deleted_account = True
                    account.save()
                    logout(request)
                    messages.success(request,'Your Account has been deleted, For any assistance please contact the Customer Service')
                    return redirect('core:index')
                else:
                    messages.error(request,'Incorrect pin number')
                    return redirect('account:account')
            else:
                messages.error(request,'You have balance amount in one of your cards, Please move the money first,then only try to delete account.')
                return redirect('account:account')
            
        else:
            messages.error(request,'You have balance amount in one your account, Please move the money first.')
            return redirect('')




@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)


    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc = None

    if request.method == 'POST':
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, 'KYC Form submitted successsfully. In review now!')
            account.kyc_submitted = True
            account.save()
            return redirect('core:index')
    else:
        form = KYCForm(instance=kyc)
    context = {
        'account':account,
        'form':form,
        'kyc':kyc,
    }
    return render(request, 'account/kyc_form.html',context)



def is_2fa(request):
    user = request.user
    
    if user.is_2fa == True:
        user.is_2fa = False
        user.save()
        messages.success(request,'You disabled the 2FA')
        return redirect('account:account')
    else:
        user.is_2fa = True
        user.save()
        messages.success(request,'You Enabled the 2FA')
        return redirect('account:account')
    


def change_pin_number(request):
    user = request.user
    kyc = KYC.objects.get(user=user)

    user.otp = random.randint(100000,999999)
    user.save()

    def format_phone_number(phone_number):
        phone_number = phone_number.replace(" ", "")
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        return phone_number
    user.user_id = random.randint(12345678,99999999)
    user.save()
    
    phone_number = format_phone_number(kyc.mobile)

    message_handler = MessageHandler(phone_number,user.otp).send_otp_on_phone()
    messages.success(request,'The OTP to change the pin number is sent to your phone number.')
    return redirect('account:pin_change_confirm_otp',user.user_id)




def pin_change_confirm_otp(request,user_id):
    user = User.objects.get(user_id=user_id)
    account = Account.objects.get(user=user)

    if request.method == 'POST':
        user = User.objects.get(user_id=user_id)
        otp_number = request.POST.get('otp_number')

        if otp_number == user.otp:
            messages.get_messages(request).used = True
            new_pin = random.randint(1111,9999)
            account.pin_number = new_pin
            account.save()
            messages.success(request, 'You changed your Pin Succesfully')
            return redirect('account:dashboard')
        else:
            messages.error(request,'Incorrect OTP,Try again.')
    
    context = {
        'user_id':user_id
    }
    
    return render(request,'account/pin_change_confirm_otp.html',context)