import uuid
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




ACCOUNT_STATUS = (
    ("active", "Active"),
    ("pending", "Pending"),
    ("in-active", "In-active")
)

ACCOUNT_COUNTRY_CURRENCY = (
    ("INR", "INR"),
    ("USD", "USD"),
)

ACCOUNT_IFSC = (
    ("EPDW00902", "EPDW00902"),
)

ACCOUNT_SWIFT = (
    ("EPDWINKL902", "EPDWINKL902"),
)

MARITAL_STATUS = (
    ("married", "Married"),
    ("single", "Single"),
    ("other", "Other")
)

GENDER = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other")
)


IDENTITY_TYPE = (
    ("national_id_card", "National ID Card"),
    ("drivers_licence", "Drives Licence"),
    ("international_passport", "International Passport")
)



def user_directory_path(instance,filename):
    ext = filename.split('.')[-1]
    filename = '%s_%s' % (instance.id,ext)
    return 'user_{0}/{1}'.format(instance.user.id,filename)


class Account(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    account_number = ShortUUIDField(unique=True,length=10, max_length=25, prefix='INR',alphabet='1234567890')
    account_id = ShortUUIDField(unique=True,length=7, max_length=25, prefix='DEX',alphabet='1234567890')
    pin_number = ShortUUIDField(unique=True,length=4, max_length=7,alphabet='1234567890')
    ref_code = ShortUUIDField(unique=True,length=10, max_length=20,alphabet='abcdefgh1234567890')
    account_status = models.CharField(max_length=100, choices=ACCOUNT_STATUS, default='in-active')
    date = models.DateTimeField(auto_now_add=True)
    kyc_submitted = models.BooleanField(default=False)
    kyc_confirmed = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='recommended_by')
    deleted_account = models.BooleanField(default=False )
    credit_card_count = models.IntegerField(default=0, blank=True, null=True)
    debit_card_count = models.IntegerField(default=0, blank=True, null=True)
    account_currency = models.CharField(max_length=10,choices=ACCOUNT_COUNTRY_CURRENCY,default='INR')
    ifsc_code = models.CharField(max_length=11,choices=ACCOUNT_IFSC,default='EPDWIN00902')
    swift_code = models.CharField(max_length=11,choices=ACCOUNT_SWIFT,default='EPDWINKL902')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user}"
    

class KYC(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='kyc', default='default.jpg')
    marrital_status = models.CharField(choices=MARITAL_STATUS,max_length=40)
    gender = models.CharField(choices=GENDER, max_length=25)
    identity_type = models.CharField(choices=IDENTITY_TYPE, max_length=50)
    identity_image = models.ImageField(upload_to='KYC', null=True, blank=True)
    date_of_birth = models.DateTimeField(auto_now_add=False)
    signature = models.ImageField(upload_to='kyc')

    #Address
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    #Contact Detail
    mobile = models.CharField(max_length=25)
    is_mobile_verfied = models.BooleanField(default=False)
    fax = models.CharField(max_length=25)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user}"

        

@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_account(sender, instance, **kwargs):
    instance.account.save()

post_save.connect(create_account, sender=User)
post_save.connect(save_account, sender=User)



class AccountForex(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    account_number = ShortUUIDField(unique=True,length=10, max_length=25, prefix='USD',alphabet='1234567890')
    account_id = ShortUUIDField(unique=True,length=7, max_length=25, prefix='DEX',alphabet='1234567890')
    pin_number = ShortUUIDField(unique=True,length=4, max_length=7,alphabet='1234567890')
    account_status = models.CharField(max_length=100, choices=ACCOUNT_STATUS, default='active')
    date = models.DateTimeField(auto_now_add=True)
    deleted_account = models.BooleanField(default=False )
    debit_card_count = models.IntegerField(default=0, blank=True, null=True)
    account_currency = models.CharField(max_length=10,choices=ACCOUNT_COUNTRY_CURRENCY,default='USD')
    ifsc_code = models.CharField(max_length=11,choices=ACCOUNT_IFSC,default='EPDWIN00902')
    swift_code = models.CharField(max_length=11,choices=ACCOUNT_SWIFT,default='EPDWINKL902')



    class Meta:
        ordering = ['-date']
        verbose_name = "Account Forex"
        verbose_name_plural = "Forex Accounts"


    def __str__(self):
        return f"{self.user}"



