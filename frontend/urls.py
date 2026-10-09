from django.urls import path

from .views import (
    login_page,
    register_page,
    dashboard_page,
    cards_page,
    payment_page,
    transactions_page,
    admin_summary_page,
)


urlpatterns = [
    path("", login_page, name="login_page"),
    path("login/", login_page, name="login_page"),
    path("register/", register_page, name="register_page"),
    path("dashboard/", dashboard_page, name="dashboard_page"),
    path("cards/", cards_page, name="cards_page"),
    path("payment/", payment_page, name="payment_page"),
    path(
        "transactions/",
        transactions_page,
        name="transactions_page",
    ),

    path(
        "admin-summary/",
        admin_summary_page,
        name="admin_summary_page",
    ),
]