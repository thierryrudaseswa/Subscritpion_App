from celery import shared_task
from django.utils import timezone
from subscriptions.models import Subscription


@shared_task
def check_subscription_status():
    now = timezone.now()
    expired = Subscription.objects.filter(status="active", end_date__lt=now)
    expired.update(status="expired")
    return f"Updated {expired.count()} expired subscriptions"
