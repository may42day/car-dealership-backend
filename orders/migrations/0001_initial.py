# Generated by Django 4.2.5 on 2023-09-05 10:46

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("dealers", "0001_initial"),
        ("customers", "0001_initial"),
        ("suppliers", "0001_initial"),
        ("cars", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TotalSupplierPurchase",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("amount", models.PositiveBigIntegerField(default=0)),
                ("dealer", models.ManyToManyField(to="dealers.dealer")),
                (
                    "supplier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="total_purchases",
                        to="suppliers.supplier",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TotalDealerPurchase",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("amount", models.PositiveBigIntegerField(default=0)),
                ("customer", models.ManyToManyField(to="customers.customer")),
                (
                    "dealer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="total_purchases",
                        to="dealers.dealer",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DealerDealsHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("amount", models.PositiveIntegerField(default=1)),
                ("price_per_one", models.BigIntegerField()),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("car", models.ManyToManyField(to="cars.car")),
                (
                    "dealer",
                    models.ManyToManyField(related_name="history", to="dealers.dealer"),
                ),
                (
                    "supplier",
                    models.ManyToManyField(
                        related_name="dealer_history", to="suppliers.supplier"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CustomerOffer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("max_price", models.PositiveBigIntegerField()),
                (
                    "place",
                    django_countries.fields.CountryField(
                        blank=True, max_length=2, null=True
                    ),
                ),
                (
                    "characteristic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="cars.carcharacteristic",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CustomerDealsHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("amount", models.PositiveIntegerField(default=1)),
                ("price_per_one", models.BigIntegerField()),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("car", models.ManyToManyField(to="cars.car")),
                (
                    "customer",
                    models.ManyToManyField(
                        related_name="history", to="customers.customer"
                    ),
                ),
                (
                    "dealer",
                    models.ManyToManyField(
                        related_name="customer_history", to="dealers.dealer"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
