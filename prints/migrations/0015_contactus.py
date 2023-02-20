# Generated by Django 4.1.4 on 2023-02-20 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prints', '0014_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField(max_length=200)),
            ],
            options={
                'ordering': ('-modified_on', '-created_on'),
                'get_latest_by': 'modified_on',
                'abstract': False,
            },
        ),
    ]
