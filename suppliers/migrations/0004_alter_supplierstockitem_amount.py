# Generated by Django 4.2.5 on 2023-10-08 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("suppliers", "0003_supplier_user_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supplierstockitem",
            name="amount",
            field=models.PositiveBigIntegerField(),
        ),
    ]
