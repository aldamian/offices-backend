from django.contrib import admin
from .models import User, Remote_Request, Desk_Request, Building, Office, Desk, Office_Image, User_Image
from django.forms import TextInput, Textarea
from django.db import models


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'first_name', 'last_name', 'desk_id', 
                    'gender', 'birth_date', 'nationality', 'remote_percentage', 'is_superuser')
    # prepopulated_fileds = {}

admin.site.register(Building)
admin.site.register(Office)
admin.site.register(Desk)
admin.site.register(Remote_Request)
admin.site.register(Desk_Request)
admin.site.register(Office_Image)
admin.site.register(User_Image)

