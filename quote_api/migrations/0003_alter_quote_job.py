# Generated by Django 4.0.2 on 2022-02-28 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote_api', '0002_remove_quote_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='job',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]