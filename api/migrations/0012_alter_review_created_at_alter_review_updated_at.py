# Generated by Django 5.1.6 on 2025-03-04 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0011_rename_webiste_restaurant_website"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="review",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
