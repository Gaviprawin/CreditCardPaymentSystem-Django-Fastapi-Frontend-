import csv

from django.contrib import admin
from django.http import HttpResponse
from .models import AdminActivityLog


from .models import Transaction


def export_transactions(modeladmin, request, queryset):

    response = HttpResponse(
        content_type="text/csv"
    )

    response["Content-Disposition"] = (
        'attachment; filename="transactions.csv"'
    )

    writer = csv.writer(response)

    writer.writerow(
        [
            "Transaction ID",
            "Username",
            "Card Last 4",
            "Amount",
            "Status",
            "Created At",
            "Completed At",
        ]
    )

    for transaction in queryset:

        writer.writerow(
            [
                transaction.transaction_id,
                transaction.user.username,
                (
                    transaction.card.last_four_digits
                    if transaction.card
                    else ""
                ),
                transaction.amount,
                transaction.status,
                transaction.created_at,
                transaction.completed_at,
            ]
        )

    return response


export_transactions.short_description = (
    "Export selected transactions to CSV"
)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        "transaction_id",
        "user",
        "card",
        "amount",
        "status",
        "created_at",
        "completed_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "transaction_id",
        "user__username",
        "card__last_four_digits",
    )

    actions = [
        export_transactions
    ]


# from django.contrib import admin


@admin.register(AdminActivityLog)
class AdminActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "actor",
        "action",
        "description",
        "ip_address",
        "created_at",
    )
    list_filter = ("action", "created_at")
    search_fields = (
        "actor__username",
        "action",
        "description",
        "ip_address",
    )
    readonly_fields = (
        "actor",
        "action",
        "description",
        "ip_address",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False