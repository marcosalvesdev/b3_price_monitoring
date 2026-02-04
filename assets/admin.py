from django.contrib import admin
from assets.models import Asset


@admin.register(Asset)
class AssetsAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')
    search_fields = ('name', 'user__username')
    list_filter = ('created_at', 'updated_at')
