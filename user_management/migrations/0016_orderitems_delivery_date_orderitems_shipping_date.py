# Generated by Django 4.1.4 on 2023-04-19 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0015_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='shipping_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]