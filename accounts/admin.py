from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Account

# Inline para Account en la vista de User
class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Cuenta de Amazon'
    fk_name = 'user'

# Desregistrar User para personalizarlo
admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (AccountInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'get_amazon_user_id')
    list_filter = ('is_active', 'is_staff', 'account__amazon_user_id')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'account__amazon_user_id')
    ordering = ('username',)
    fieldsets = BaseUserAdmin.fieldsets
    add_fieldsets = BaseUserAdmin.add_fieldsets

    def get_amazon_user_id(self, obj):
        return getattr(obj.account, 'amazon_user_id', None)
    get_amazon_user_id.short_description = 'Amazon User ID'

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'amazon_user_id')
    search_fields = ('user__username', 'user__email', 'amazon_user_id')
    raw_id_fields = ('user',)
    list_filter = ('amazon_user_id',)

    def get_queryset(self, request):
        # Optimiza las consultas, especialmente si tienes muchas cuentas
        qs = super().get_queryset(request)
        return qs.select_related('user')
