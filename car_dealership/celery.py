import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_dealership.settings")

app = Celery("car_dealership")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "order-on-stock-every-10-minutes": {
        "task": "orders.tasks.regular_order_on_dealer_stock",
        "schedule": crontab(minute="*/10"),
    },
    "customer-offers-every-10-minutes": {
        "task": "orders.tasks.regular_order_by_customers",
        "schedule": crontab(minute="*/10"),
    },
    "check-cooperation-with-suppliers": {
        "task": "orders.tasks.regular_cooperation_profitability_check",
        "schedule": crontab(minute=0, hour="*/1"),
    },
}

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
