from django.urls import path

from .views import (
    PaymentView,
    TransactionListView,
    TransactionDetailView,
    AdminTransactionExportView,
    AdminDailySummaryView,
)


urlpatterns = [

    path(
        "pay/",
        PaymentView.as_view(),
        name="payment"
    ),

    path(
        "",
        TransactionListView.as_view(),
        name="transaction-list"
    ),

    path(
        "<uuid:transaction_id>/",
        TransactionDetailView.as_view(),
        name="transaction-detail"
    ),

    path(
        "admin/export/",
        AdminTransactionExportView.as_view(),
        name="admin-export"
    ),

    path(
        "admin/summary/",
        AdminDailySummaryView.as_view(),
        name="admin-summary",
    ),
]