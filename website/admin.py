from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "email", "interest", "created_at")
    list_filter = ("company_size", "created_at")
    search_fields = ("name", "email", "company", "interest", "message")
    readonly_fields = ("created_at",)
