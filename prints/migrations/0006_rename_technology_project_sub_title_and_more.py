# Generated by Django 4.1.4 on 2023-01-01 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prints', '0005_remove_service_menu'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='technology',
            new_name='sub_title',
        ),
        migrations.RemoveField(
            model_name='project',
            name='type',
        ),
    ]