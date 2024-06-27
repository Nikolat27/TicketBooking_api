# Generated by Django 5.0.6 on 2024-06-27 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticket_app", "0005_rename_passengers_type_passengers_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="passengers",
            name="age",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="If the type is adult, keep this field NULL",
                null=True,
            ),
        ),
    ]
