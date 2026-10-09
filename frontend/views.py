from django.shortcuts import render


def login_page(request):
    return render(request, "frontend/login.html")


def register_page(request):
    return render(request, "frontend/register.html")


def dashboard_page(request):
    return render(request, "frontend/dashboard.html")


def cards_page(request):
    return render(request, "frontend/cards.html")


def payment_page(request):
    return render(request, "frontend/payment.html")


def transactions_page(request):
    return render(request, "frontend/transactions.html")

def admin_summary_page(request):
    return render(request,"frontend/admin_summary.html")