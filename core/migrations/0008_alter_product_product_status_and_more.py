# Generated by Django 4.2.2 on 2023-07-23 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_product_product_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('disabled', 'Disabled'), ('In_review', 'In review'), ('draft', 'Draft'), ('rejected', 'Rejected'), ('published', 'Published')], default='In_review', max_length=10),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(5, '★★★★★'), (3, '★★★☆☆'), (1, '★☆☆☆☆'), (2, '★★☆☆☆'), (4, '★★★★☆')], default=None),
        ),
        migrations.AlterField(
            model_name='productsimages',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='p_images', to='core.product'),
        ),
    ]
