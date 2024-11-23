from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import SubscriptionPlan, Subscription
from .forms import SubscriptionForm


@login_required
def plan_list(request):
    plans = SubscriptionPlan.objects.filter(is_active=True)
    return render(request, "subscriptions/plan_list.html", {"plans": plans})


@login_required
def subscribe(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)

    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.plan = plan
            subscription.status = "active"
            subscription.start_date = timezone.now()

            # Calculate end date based on billing cycle
            if subscription.billing_cycle == "monthly":
                months = 1
            elif subscription.billing_cycle == "quarterly":
                months = 3
            else:  # annually
                months = 12

            subscription.end_date = subscription.start_date + timedelta(
                days=30 * months
            )
            subscription.amount_paid = plan.price
            subscription.save()

            messages.success(request, f"Successfully subscribed to {plan.name}!")
            return redirect("subscription_detail")
    else:
        form = SubscriptionForm(initial={"billing_cycle": plan.billing_cycle})

    return render(request, "subscriptions/subscribe.html", {"form": form, "plan": plan})


@login_required
def subscription_detail(request):
    subscriptions = Subscription.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    return render(
        request,
        "subscriptions/subscription_detail.html",
        {"subscriptions": subscriptions},
    )
