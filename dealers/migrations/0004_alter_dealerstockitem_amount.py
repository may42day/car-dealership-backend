# Generated by Django 4.2.5 on 2023-10-06 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dealers", "0003_dealer_user_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dealerstockitem",
            name="amount",
            field=models.PositiveBigIntegerField(),
        ),
    ]
