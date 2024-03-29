# Generated by Django 4.2.5 on 2023-09-19 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0002_rename_model_carcharacteristic_car_model_and_more"),
        ("dealers", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dealer",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.RemoveField(
            model_name="dealerstockitem",
            name="car",
        ),
        migrations.AlterField(
            model_name="dealerstockitem",
            name="dealer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="stock",
                to="dealers.dealer",
            ),
        ),
        migrations.AlterField(
            model_name="dealerstockitem",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="dealerstockitem",
            name="car",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.PROTECT, to="cars.car"
            ),
            preserve_default=False,
        ),
    ]
