
from .models import AdminActivityLog


def log_activity(request, action, description):
    user = getattr(request, "user", None)

    if not user or not user.is_authenticated:
        user = None

    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    ip_address = (
        forwarded_for.split(",")[0].strip()
        if forwarded_for
        else request.META.get("REMOTE_ADDR")
    )

    # Do not trust arbitrary forwarded IP headers unless
    # your reverse proxy is configured to set them securely.
    AdminActivityLog.objects.create(
        actor=user,
        action=action,
        description=description,
        ip_address=ip_address or None,
    )