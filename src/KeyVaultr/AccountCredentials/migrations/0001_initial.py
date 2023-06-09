# Generated by Django 4.2.1 on 2023-05-24 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountCredential',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('password', models.CharField(max_length=255)),
                ('website', models.CharField(max_length=255)),
                ('notes', models.TextField()),
                ('is_favorite', models.BooleanField(default=False)),
            ],
        ),
    ]
