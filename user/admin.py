from django.contrib import admin
from .models import Profile,Requests

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Profile', {
            "fields": (
                'image',
                'user'
            ),
        }),
    )
    
admin.site.register(Profile)
admin.site.register(Requests)