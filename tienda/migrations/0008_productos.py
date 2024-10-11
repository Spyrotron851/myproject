# Generated by Django 3.2.6 on 2023-03-18 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0007_alter_article_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True, verbose_name='Titulo')),
                ('content', models.CharField(max_length=80, null=True, verbose_name='Contenido')),
                ('content2', models.CharField(max_length=200, null=True, verbose_name='Contenido2')),
            ],
            options={
                'verbose_name': 'Articulo',
                'verbose_name_plural': 'Articulos',
            },
        ),
    ]
