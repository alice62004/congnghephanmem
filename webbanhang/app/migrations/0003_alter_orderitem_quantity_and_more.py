# Generated by Django 5.1.1 on 2024-11-12 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_product_image_alter_product_digital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='shippingaddress',
            unique_together={('customer', 'order')},
        ),
    ]
