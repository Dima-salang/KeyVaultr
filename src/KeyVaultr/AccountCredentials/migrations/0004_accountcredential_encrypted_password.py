# Generated by Django 4.2.1 on 2023-05-26 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccountCredentials', '0003_alter_accountcredential_notes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountcredential',
            name='encrypted_password',
            field=models.BinaryField(blank=True),
        ),
    ]
