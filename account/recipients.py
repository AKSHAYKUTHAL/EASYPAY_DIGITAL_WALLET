from django.shortcuts import render, redirect
from core.models import Transaction
from userauths.models import User
from django.db.models import Q







def recipients(request):
    user_transactions = Transaction.objects.filter(Q(sender=request.user) | Q(reciever=request.user))

    recipients = {}
    for transaction in user_transactions:
        if transaction.sender != request.user:
            if transaction.sender not in recipients:
                recipients[transaction.sender] = 1
            else:
                recipients[transaction.sender] += 1

        if transaction.reciever != request.user:
            if transaction.reciever not in recipients:
                recipients[transaction.reciever] = 1
            else:
                recipients[transaction.reciever] += 1
    
    recipient_counts = {}
    for recipient in recipients:
        recipient_count = Transaction.objects.filter(Q(sender=request.user, reciever=recipient) | Q(sender=recipient, reciever=request.user)).count()
        recipient_counts[recipient] = recipient_count

    print(f"recipients: {recipients}")
    print(f"recipient_counts: {recipient_counts}")

    context = {
        'recipients': recipients,
        'recipient_counts': recipient_counts
    }

    return render(request, 'account/recipients.html', context)



def recipient_transactions(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    user = request.user
    transactions = Transaction.objects.filter(Q(sender=user, reciever=recipient) | Q(sender=recipient, reciever=user)).order_by('-id')

    transactions_count = transactions.count()

    context = {
        'transactions': transactions,
        'recipient': recipient,
        'user': user,
        'transactions_count':transactions_count
    }
    return render(request, 'account/recipient_transactions.html', context)