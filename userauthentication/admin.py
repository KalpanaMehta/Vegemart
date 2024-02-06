from django.contrib import admin
from userauthentication.models import User,Profile
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display =['username','email','bio']

class ProfileAdmin(admin.ModelAdmin):
    list_display =['user','full_name','bio','phone']

admin.site.register(User,UserAdmin) 
admin.site.register(Profile,ProfileAdmin) 