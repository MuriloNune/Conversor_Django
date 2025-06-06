# Generated by Django 5.2 on 2025-04-27 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_file', models.FileField(upload_to='documents/')),
                ('converted_file', models.FileField(blank=True, null=True, upload_to='converted/')),
                ('converted_format', models.CharField(max_length=10)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
