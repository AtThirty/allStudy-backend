from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from rest_framework_simplejwt import token_blacklist

class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want

class AccountAdmin(UserAdmin):
    list_display = ('username', 'date_joined', 'last_login', 'is_superuser')
    search_fields = ('username', 'date_joined')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)
admin.site.register(User, AccountAdmin)
