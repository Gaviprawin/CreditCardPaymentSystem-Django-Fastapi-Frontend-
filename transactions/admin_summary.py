
from datetime import datetime, time, timedelta
from decimal import Decimal

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q
from django.http import HttpResponse
from django.utils import timezone

from .models import Transaction


@staff_member_required
def daily_payment_summary(request):
    today = timezone.localdate()

    start = timezone.make_aware(
        datetime.combine(today, time.min)
    )
    end = timezone.make_aware(
        datetime.combine(today + timedelta(days=1), time.min)
    )

    daily = Transaction.objects.filter(
        created_at__gte=start,
        created_at__lt=end,
    )

    totals = daily.aggregate(
        total_transactions=Count("id"),
        successful=Count(
            "id", filter=Q(status="SUCCESS")
        ),
        failed=Count(
            "id", filter=Q(status="FAILED")
        ),
        pending=Count(
            "id", filter=Q(status="PENDING")
        ),
        successful_amount=Sum(
            "amount", filter=Q(status="SUCCESS")
        ),
    )

    def number(value):
        return value or 0

    total_amount = number(totals["successful_amount"])
    total_transactions = number(totals["total_transactions"])
    successful = number(totals["successful"])
    failed = number(totals["failed"])
    pending = number(totals["pending"])

    html = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Daily Payment Summary</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          margin: 35px;
          background: #f4f7fb;
          color: #172033;
        }}
        h1 {{ margin-bottom: 5px; }}
        .date {{ color: #64748b; margin-bottom: 25px; }}
        .cards {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
          gap: 16px;
        }}
        .card {{
          padding: 22px;
          background: white;
          border-radius: 12px;
          box-shadow: 0 3px 14px #0000000d;
        }}
        .label {{ color: #64748b; font-size: 14px; }}
        .value {{ font-size: 28px; font-weight: bold; margin-top: 12px; }}
        a {{ display: inline-block; margin-top: 25px; }}
      </style>
    </head>
    <body>
      <h1>Daily Payment Summary</h1>
      <div class="date">Date: {today.isoformat()}</div>
      <div class="cards">
        <div class="card">
          <div class="label">Total Transactions</div>
          <div class="value">{total_transactions}</div>
        </div>
        <div class="card">
          <div class="label">Successful Payments</div>
          <div class="value">{successful}</div>
        </div>
        <div class="card">
          <div class="label">Failed Payments</div>
          <div class="value">{failed}</div>
        </div>
        <div class="card">
          <div class="label">Pending Payments</div>
          <div class="value">{pending}</div>
        </div>
        <div class="card">
          <div class="label">Successful Payment Amount</div>
          <div class="value">₹{total_amount}</div>
        </div>
      </div>
      <a href="/admin/">Back to Django Admin</a>
    </body>
    </html>
    """

    return HttpResponse(html)