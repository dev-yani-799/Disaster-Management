# Generated by Django 4.2.3 on 2024-03-19 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_certificate_estimate'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='alert',
            name='longitude',
            field=models.FloatField(null=True),
        ),
    ]
