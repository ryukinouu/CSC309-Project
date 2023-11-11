# Generated by Django 4.2.7 on 2023-11-11 01:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_remove_petseeker_user_remove_petshelter_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="myuser",
            name="is_seeker",
            field=models.BooleanField(default=False, verbose_name="Is seeker"),
        ),
        migrations.AddField(
            model_name="myuser",
            name="is_shelter",
            field=models.BooleanField(default=False, verbose_name="Is shelter"),
        ),
    ]
