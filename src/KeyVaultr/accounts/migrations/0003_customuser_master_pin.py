# Generated by Django 4.2.1 on 2023-05-25 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='master_pin',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
