# Generated by Django 3.2.6 on 2022-08-11 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0006_alter_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(default=None, upload_to='articles', verbose_name='Imagen'),
        ),
    ]
