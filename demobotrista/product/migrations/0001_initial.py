# Generated by Django 4.2.13 on 2024-06-02 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField()),
                ('currency', models.CharField(choices=[('TWD', 'New Taiwan Dollar')], default='TWD', max_length=3)),
            ],
            options={
                'permissions': [('can_manage_products', 'Can manage product')],
            },
        ),
    ]
