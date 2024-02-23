from django.db import models
from django.db.models.query import QuerySet
from django_countries.fields import CountryField

from users.models import UserProfile


class BaseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class BaseModelManager(models.Manager):
    """
    Customized manager for BaseModel.
    """

    def get_queryset(self, is_active=True) -> QuerySet:
        """Overrided queryset for objects.
        By default returns only active instances with active=True.
        """
        return super().get_queryset().filter(is_active=is_active)


class BaseModel(models.Model):
    """
    A abstract class for models with common fields

    Attributes
    ----------
    is_active : BooleanField
        indicates removed instance
    created_at : DateTimeField
        date and time of instance creation
    updated_at : DateTimeField
        date and time of of instance update

    """

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # objects = BaseModelManager()

    class Meta:
        abstract = True

    def delete(self):
        """
        Function for soft deleting the entries.
        It changes is_active attribute to True just to indicate that instance was delleted

        """

        self.is_active = True
        self.save()


class Company(BaseModel):
    """
    A abstract class for companies models

    Attributes
    ----------
    name : CharField
        name of company
    balance : PositiveBigIntegerField
        current company's balance
    place : CountryField
        company location
    foundation_date : DateField
        date of company foundation
    user_profile : OneToOneField
        relation to user profile
    """

    name = models.CharField(max_length=255)
    balance = models.PositiveBigIntegerField(default=0)
    place = CountryField(blank=True, null=True)
    foundation_date = models.DateField(blank=True, null=True)
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.pk} {self.name}"


class AmountCalculator(models.Model):
    """
    An abstract class providing interface for changing amount of some model.
    """

    amount = models.PositiveBigIntegerField(default=0)

    class Meta:
        abstract = True

    def add_amount(self, amount: int):
        """
        Function to update total deals amount.
        """
        self.amount += amount
        self.save()
