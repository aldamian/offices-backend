from django.contrib import admin
from .models import User, Request, Building, Office, Desk, Office_Image
from django.forms import TextInput, Textarea
from django.db import models


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'role', 'first_name')
    list_filter = ('email', 'first_name', 'role')
    list_display = ('email', 'role', 'first_name', 'last_name', 'office_id', 'building_id',
                    'gender', 'birth_date', 'nationality', 'remote_percentage', 'is_superuser', 'is_active', 'is_staff')
    # prepopulated_fileds = {}

admin.site.register(Building)
admin.site.register(Office)
admin.site.register(Desk)
admin.site.register(Request)
admin.site.register(Office_Image)

