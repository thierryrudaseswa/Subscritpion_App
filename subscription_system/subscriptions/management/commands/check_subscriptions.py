from django.core.management.base import BaseCommand
from django.utils import timezone
from subscriptions.models import Subscription


class Command(BaseCommand):
    help = "Check and update subscription statuses"

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Update expired subscriptions
        expired = Subscription.objects.filter(status="active", end_date__lt=now)

        expired_count = expired.update(status="expired")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully updated {expired_count} expired subscriptions"
            )
        )
