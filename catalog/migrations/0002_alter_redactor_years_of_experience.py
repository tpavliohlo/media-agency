# Generated by Django 4.2.17 on 2025-01-03 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redactor',
            name='years_of_experience',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
