# Generated by Django 4.2.5 on 2023-09-20 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tender_app', '0006_alter_tender_types_of_work_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='favourites',
            field=models.ManyToManyField(blank=True, to='tender_app.worker'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='feedbacks',
            field=models.ManyToManyField(blank=True, to='tender_app.feedback'),
        ),
    ]
