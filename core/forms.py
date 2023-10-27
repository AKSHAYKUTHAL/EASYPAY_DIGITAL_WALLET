from django import forms
from core.models import CreditCard,DebitCard

class CreditCardForm(forms.ModelForm):

    class Meta:
        model = CreditCard
        fields = [ 'card_type','card_tier']


class DebitCardForm(forms.ModelForm):

    class Meta:
        model = DebitCard
        fields = [ 'card_type','card_tier']