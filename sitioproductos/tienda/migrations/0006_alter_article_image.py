# Generated by Django 3.2.6 on 2022-08-11 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0005_auto_20220811_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(default='null', upload_to='articles', verbose_name='Imagen'),
        ),
    ]
