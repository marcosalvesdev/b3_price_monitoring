from django.contrib import admin

from tunnels.models import PriceTunnel


@admin.register(PriceTunnel)
class PriceTunnelAdmin(admin.ModelAdmin):
    list_display = ('asset', 'upper_limit', 'lower_limit', 'check_interval_minutes', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('asset__name', 'asset__ticker')
    ordering = ('-created_at',)
