"""
doc string goes here
"""

__all__ = []

# Standard library imports.

# Related third party imports.
from django.contrib import admin

# Local application/library specific imports.
from .models import Provider, Currency, CurrencyExchangeRate


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_editable = ('name', )


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_editable = ('name', )


class ReadOnlyAdminMixin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('provider', 'from_currency', 'to_currency',
                    'rate', 'on_date')
    list_filter = ('provider', 'from_currency', 'to_currency')

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        else:
            return False


admin.site.register(Provider, ProviderAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyExchangeRate, CurrencyExchangeRateAdmin)
