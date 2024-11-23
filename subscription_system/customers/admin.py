from django.contrib import admin
from .models import Customer, InteractionLog


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "phone")
    search_fields = ("user__username", "user__email", "company_name")


@admin.register(InteractionLog)
class InteractionLogAdmin(admin.ModelAdmin):
    list_display = ("customer", "interaction_type", "created_at")
    list_filter = ("interaction_type",)
