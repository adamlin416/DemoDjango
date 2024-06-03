from django.urls import path

from . import views

urlpatterns = [
    path("", views.OrderListAPIView.as_view(), name="order-list"),
]
