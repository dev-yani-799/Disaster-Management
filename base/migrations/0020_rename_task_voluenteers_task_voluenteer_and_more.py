# Generated by Django 5.0.3 on 2024-03-22 08:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0019_task_voluenteers"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Task_voluenteers",
            new_name="Task_voluenteer",
        ),
        migrations.AlterField(
            model_name="task_voluenteer",
            name="userid",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
