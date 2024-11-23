from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"customers", views.CustomerViewSet, basename="customer")
router.register(r"interactions", views.InteractionLogViewSet, basename="interaction")

urlpatterns = [
    path("", include(router.urls)),
]
