# Generated by Django 4.2.2 on 2023-07-21 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_wishlist_wishlist_product_remove_product_tags_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.vendor'),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(choices=[('shipped', 'Shipped'), ('process', 'Processing'), ('delivered', 'Delivered')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('draft', 'Draft'), ('rejected', 'Rejected'), ('disabled', 'Disabled'), ('published', 'Published'), ('In_review', 'In review')], default='In_review', max_length=10),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(5, '★★★★★'), (4, '★★★★☆'), (1, '★☆☆☆☆'), (3, '★★★☆☆'), (2, '★★☆☆☆')], default=None),
        ),
    ]
