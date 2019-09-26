from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Node, Level


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'address', 'balance', 'display_level', 'level_expire_time')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'inviter_id')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Wallet', {'fields': ('address', 'balance')}),
        ('ss_config', {'fields': ('level', 'level_expire_time', 'port', 'port_password', 'batch')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'), }),
        ('SS-CONFIG', {'fields': {'level', 'level_expire_time', 'port', 'port_password', 'batch'}})
    )


# Register your models here.
# admin.site.register(User, MyUserAdmin)

admin.site.register(Node)

admin.site.register(Level)
