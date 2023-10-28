from django.contrib import admin
from userauths.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'email','is_2fa','otp','user_id'] 


admin.site.register(User,UserAdmin)
