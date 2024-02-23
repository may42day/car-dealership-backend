import pytest
from ddf import G

from customers.models import Customer


@pytest.mark.django_db
def test_customer_queryset_active():
    """
    Tests 'active' queryset method. Should return customers only with is_active=True.
    """
    active_customer = G(Customer, is_active=True)
    inactive_customer = G(Customer, is_active=False)

    active_customers = Customer.objects.active()
    assert active_customer in active_customers
    assert inactive_customer not in active_customers
