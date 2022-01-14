# Generated by Django 4.0.1 on 2022-01-10 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_order_time_create_alter_order_order_description_and_more'),
        ('cart', '0008_alter_cartitem_order_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='order_items', to='order.order'),
        ),
    ]