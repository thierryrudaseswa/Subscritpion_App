from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import SubscriptionPlan, Subscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "billing_cycle", "is_active", "subscriber_count")
    list_filter = ("is_active", "billing_cycle")
    search_fields = ("name", "description")

    def subscriber_count(self, obj):
        count = Subscription.objects.filter(plan=obj, status="active").count()
        return format_html(
            '<a href="{}?plan__id__exact={}&status__exact=active">{} subscribers</a>',
            reverse("admin:subscriptions_subscription_changelist"),
            obj.id,
            count,
        )

    subscriber_count.short_description = "Active Subscribers"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "customer_info",
        "plan_info",
        "amount_paid",
        "status",
        "start_date",
        "end_date",
    )
    list_filter = ("status", "billing_cycle", "plan", "auto_renew")
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    date_hierarchy = "start_date"
    readonly_fields = ("created_at", "updated_at")
    actions = ["mark_as_active", "mark_as_cancelled"]

    fieldsets = (
        ("Customer Information", {"fields": ("user", "plan", "status")}),
        ("Billing Details", {"fields": ("billing_cycle", "amount_paid", "auto_renew")}),
        ("Subscription Period", {"fields": ("start_date", "end_date")}),
        ("Additional Information", {"fields": ("notes", "created_at", "updated_at")}),
    )

    def customer_info(self, obj):
        return format_html(
            "<div><strong>{}</strong><br>"
            "<small>{}</small><br>"
            "<small>Phone: {}</small></div>",
            obj.user.get_full_name() or obj.user.username,
            obj.user.email,
            obj.user.profile.phone if hasattr(obj.user, "profile") else "N/A",
        )

    customer_info.short_description = "Customer"

    def plan_info(self, obj):
        return format_html(
            "<div><strong>{}</strong><br>" "<small>${}/{}</small></div>",
            obj.plan.name,
            obj.amount_paid,
            obj.get_billing_cycle_display(),
        )

    plan_info.short_description = "Plan Details"

    def mark_as_active(self, request, queryset):
        queryset.update(status="active")

    mark_as_active.short_description = "Mark selected subscriptions as active"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status="cancelled")

    mark_as_cancelled.short_description = "Mark selected subscriptions as cancelled"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["start_date"].initial = timezone.now()
        if not obj:  # Only for new subscriptions
            form.base_fields["status"].initial = "active"
        return form

    def save_model(self, request, obj, form, change):
        if not change:  # Only for new subscriptions
            if not obj.amount_paid:
                obj.amount_paid = obj.plan.price
        super().save_model(request, obj, form, change)
