# Generated by Django 4.2.6 on 2023-11-17 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_remove_commentonapplication_reply_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentonapplication',
            name='commenter_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='commentonshelter',
            name='commenter_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
