# Generated by Django 4.0.1 on 2022-01-06 14:58

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_remove_cartitem_item_cartitem_product_and_more'),
        ('product', '0008_alter_category_title_alter_product_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_img',
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('IS', 'In Stock'), ('OS', 'Out Stock')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, null=True, populate_from='title', unique=True),
        ),
        migrations.DeleteModel(
            name='Variation',
        ),
    ]