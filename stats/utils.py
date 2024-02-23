from datetime import date
from typing import Union

from customers.models import Customer
from dealers.models import Dealer
from suppliers.models import Supplier


def get_filter_params(
    field_name: str,
    model_obj: Union[Customer, Dealer, Supplier],
    start_date: str = None,
    end_date: str = None,
) -> dict:
    """
    Function to parse and check date from string
    and then create dict which represents filter's parameters for model queryset.
    """
    params = {
        field_name: model_obj,
    }
    if start_date:
        start_date = date.fromisoformat(start_date)
    if end_date:
        end_date = date.fromisoformat(end_date)
    if start_date and end_date and start_date > end_date:
        raise ValueError("End_date must be greater or equal than start_date")

    if start_date and end_date:
        params["date__range"] = (start_date, end_date)
    elif start_date and not end_date:
        params["date__gt"] = start_date
    elif not start_date and end_date:
        params["date__lt"] = end_date

    return params
