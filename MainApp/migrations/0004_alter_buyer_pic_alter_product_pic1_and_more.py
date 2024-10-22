# Generated by Django 5.0.1 on 2024-02-07 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0003_alter_buyer_pic_alter_product_pic1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='pic',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pic1',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pic2',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pic3',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='pic',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images'),
        ),
    ]
