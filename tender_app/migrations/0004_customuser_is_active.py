# Generated by Django 4.2.5 on 2023-09-10 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tender_app', '0003_alter_customuser_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
