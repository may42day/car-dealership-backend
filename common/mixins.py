class DealerOwnerMixin:
    """
    Mixin to add specified dealer as object owner.
    """

    def perform_create(self, serializer):
        serializer.save(dealer=self.request.user.dealer)


class SupplierOwnerMixin:
    """
    Mixin to add specified supplier as object owner.
    """

    def perform_create(self, serializer):
        serializer.save(supplier=self.request.user.supplier)


class CustomerOwnerMixin:
    """
    Mixin to add specified customer as object owner.
    """

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer_profile)
