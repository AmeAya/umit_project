from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import *


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('email',)
    list_filter = ()
    search_fields = ('email',)
    ordering = ('-id',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'type')}),
        ('Subscription', {'fields': ('is_subscribed', 'expired_date',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'is_subscribed',
                'expired_date',
                'is_staff',
                'is_superuser',
                'is_active',
            )}
         ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(
    [
        Bundle,
        City,
        Company,
        Feedback,
        Reply,
        Section,
        Subsection,
        Tender,
        TenderDoc,
        Worker,
        WorkerDoc
    ]
)
