from django.db.models.signals import post_save
from django.dispatch import receiver

from customers.models import Customer
from dealers.models import Dealer
from suppliers.models import Supplier
from users.models import UserProfile
from users.tasks import email_account_confirmation


@receiver(post_save, sender=UserProfile)
def user_created_handler(
    sender: UserProfile, instance: UserProfile, created: bool, *args, **kwargs
):
    """
    Signal handler after user registration.

    Creates Customer/Dealer/Supplier profile based on UserProfile role.
    Creates task to send email letter to account confirmation.

    Parameters
    ----------
    sender: UserProfile
        sender model.
    instance: UserProfile
        instance of UserProfile.
    created: bool
        represents user creation.
        True if user was creathed. Or False if it just an update.
    *args
        additional positional arguments.
    **kwargs
        additional keyword arguments.
    """
    if created:
        if instance.role == sender.CUSTOMER:
            if instance.first_name or instance.last_name:
                name = " ".join([instance.first_name, instance.last_name]).strip()
            else:
                name = instance.username
            Customer.objects.create(user_profile=instance, name=name)

        elif instance.role == sender.DEALER:
            name = f"Company {instance.pk}"
            Dealer.objects.create(user_profile=instance, name=name)

        elif instance.role == sender.SUPPLIER:
            name = f"Company {instance.pk}"
            Supplier.objects.create(user_profile=instance, name=name)
        else:
            print("Unreachable")
            return None

        email_account_confirmation.delay(instance.pk)
