# Generated by Django 4.1.4 on 2023-02-19 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0014_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=5),
        ),
    ]