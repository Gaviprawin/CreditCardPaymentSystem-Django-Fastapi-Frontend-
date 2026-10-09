from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from transactions.admin_summary import daily_payment_summary


urlpatterns = [

    # Frontend
    path(
        "",
        include("frontend.urls")
    ),

    path(
        "admin/payment-summary/",
        daily_payment_summary,
        name="daily-payment-summary",
    ),

    # Admin
    path(
        "admin/",
        admin.site.urls
    ),

    # Authentication API
    path(
        "api/accounts/",
        include("accounts.urls")
    ),

    # Card API
    path(
        "api/cards/",
        include("cards.urls")
    ),

    # Transaction API
    path(
        "api/transactions/",
        include("transactions.urls")
    ),

    # JWT refresh
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
]