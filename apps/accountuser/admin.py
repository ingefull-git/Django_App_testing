from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accountuser.models import UserAccount


class AccountAdmin(UserAdmin):
    ordering          = ('-created', 'email',)
    search_fields     = ('email', 'username',)
    list_filter       = ('email', 'username', 'is_admin', 'is_staff', 'is_superuser', 'is_active',)
    list_display      = ('email', 'username', 'created', 'login', 'is_admin', 'is_staff', 'is_superuser', 'is_active')
    readonly_fields   = ('id', 'created', 'login',)
    fieldsets         = (
                            (None, {'fields':('email', 'username','created','login',)}),
                            ('Permissions', {'fields':('is_staff', 'is_active', 'is_admin',)}),
                            ('Personal', {'fields':('is_superuser',)})
                        )
    add_fieldsets     = (
                            (None, {
                                'classes':('wide',),
                                'fields': ('email', 'username', 'password1', 'password2', 'created', 'login')}),
                        )


admin.site.register(UserAccount, AccountAdmin)