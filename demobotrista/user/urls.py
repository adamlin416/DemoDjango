from django.urls import path

from .views import UserDetailAPIView, UserListAPIView

urlpatterns = [
    path("", UserListAPIView.as_view(), name="user-list"),
    path("<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
]
