from django.urls import path, re_path
from django.urls import include
from django.contrib.auth import views as auth_views
from accounts.views import AccountProfileModelTemplateView, AccountProfileModelDetailView
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
    path("", AccountProfileModelTemplateView.as_view(), name="accounts-app-v1-index"),
    path("<int:pk>/", AccountProfileModelDetailView.as_view(), name="accounts-app-v1-detail"),
]