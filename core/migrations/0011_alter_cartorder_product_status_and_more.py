# Generated by Django 4.2.2 on 2023-07-23 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_cartorder_product_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(choices=[('delivered', 'Delivered'), ('shipped', 'Shipped'), ('process', 'Processing')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('In_review', 'In review'), ('disabled', 'Disabled'), ('rejected', 'Rejected'), ('draft', 'Draft'), ('published', 'Published')], default='In_review', max_length=10),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='review', to='core.product'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(2, '★★☆☆☆'), (4, '★★★★☆'), (3, '★★★☆☆'), (5, '★★★★★'), (1, '★☆☆☆☆')], default=None),
        ),
    ]
