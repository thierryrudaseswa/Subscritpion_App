from django.urls import path
from . import views

urlpatterns = [
    path("", views.plan_list, name="plan_list"),
    path("subscribe/<int:plan_id>/", views.subscribe, name="subscribe"),
    path("my-subscriptions/", views.subscription_detail, name="subscription_detail"),
]
