from django.contrib import admin

from assets.models import Asset


@admin.register(Asset)
class AssetsAdmin(admin.ModelAdmin):
    list_display = ("name", "symbol", "type", "user", "is_active", "created_at", "updated_at")
    search_fields = ("name", "symbol", "user__username")
    list_filter = ("type", "is_active", "created_at", "updated_at")
