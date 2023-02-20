# Generated by Django 4.1.4 on 2022-12-30 03:12

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('image', models.ImageField(default='no-image.png', upload_to='Media/blog')),
                ('tags', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.BooleanField(default=True)),
                ('meta_keywords', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=20, null=True)),
                ('info_email', models.CharField(blank=True, max_length=50, null=True)),
                ('team_email', models.CharField(blank=True, max_length=50, null=True)),
                ('career_email', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('state', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('pin_code', models.CharField(blank=True, max_length=200, null=True)),
                ('instagram', models.CharField(blank=True, max_length=200, null=True)),
                ('facebook', models.CharField(blank=True, max_length=200, null=True)),
                ('youtube', models.CharField(blank=True, max_length=200, null=True)),
                ('twitter', models.CharField(blank=True, max_length=200, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('absolute_url', models.CharField(blank=True, max_length=255, null=True)),
                ('has_submenu', models.BooleanField(default=False)),
                ('rank', models.IntegerField(default=1)),
                ('background_image', models.FileField(blank=True, null=True, upload_to='Media/menu')),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('case_study', 'Case Study'), ('portfolio', 'Portfolio')], default='portfolio', max_length=10)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('tag', models.CharField(blank=True, max_length=255, null=True)),
                ('technology', models.CharField(blank=True, max_length=255, null=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='Media/project')),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=200, null=True)),
                ('logo', models.FileField(blank=True, null=True, upload_to='Media/logo')),
                ('office_time', models.CharField(blank=True, max_length=200, null=True)),
                ('office_day', models.CharField(blank=True, max_length=200, null=True)),
                ('website', models.CharField(blank=True, max_length=200, null=True)),
                ('technology_title', models.CharField(blank=True, max_length=200, null=True)),
                ('technology_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='Media/technology')),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ValidPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Submenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('absolute_url', models.CharField(blank=True, max_length=255, null=True)),
                ('background_image', models.FileField(blank=True, null=True, upload_to='Media/menu')),
                ('status', models.BooleanField(default=True)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prints.menu')),
            ],
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('welcome_message', models.CharField(blank=True, max_length=255, null=True)),
                ('heading', models.CharField(blank=True, max_length=255, null=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='Media/slider')),
                ('status', models.BooleanField(default=True)),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prints.menu')),
                ('sub_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prints.submenu')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='Media/service')),
                ('status', models.BooleanField(default=True)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prints.menu')),
            ],
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='Media/industry')),
                ('status', models.BooleanField(default=True)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prints.menu')),
            ],
        ),
    ]
