# Generated by Django 4.2.2 on 2023-07-29 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_address_phone_number_alter_address_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(choices=[('delivered', 'Delivered'), ('processing', 'Processing'), ('shipped', 'Shipped')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('disabled', 'Disabled'), ('draft', 'Draft'), ('published', 'Published'), ('rejected', 'Rejected'), ('In_review', 'In review')], default='In_review', max_length=10),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(5, '★★★★★'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (1, '★☆☆☆☆'), (4, '★★★★☆')], default=None),
        ),
    ]