# Generated by Django 3.2.12 on 2023-07-31 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check', '0002_checksingle'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutputFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('output', models.FileField(default='proxy_geoip.csv', upload_to='')),
            ],
        ),
    ]