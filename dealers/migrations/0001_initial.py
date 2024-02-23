# Generated by Django 4.2.5 on 2023-09-05 10:46

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("customers", "0001_initial"),
        ("suppliers", "0001_initial"),
        ("cars", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Dealer",
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
                ("name", models.CharField(max_length=255)),
                ("balance", models.PositiveBigIntegerField(default=0)),
                ("place", django_countries.fields.CountryField(max_length=2)),
                ("foundation_date", models.DateField(blank=True, null=True)),
                (
                    "car_characteristics",
                    models.ManyToManyField(to="cars.carcharacteristic"),
                ),
                ("customers", models.ManyToManyField(to="customers.customer")),
                ("suppliers", models.ManyToManyField(to="suppliers.supplier")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DealerStockItem",
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
                ("amount", models.PositiveIntegerField()),
                ("price_per_one", models.DecimalField(decimal_places=2, max_digits=10)),
                ("car", models.ManyToManyField(to="cars.car")),
                (
                    "dealer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dealers.dealer"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
