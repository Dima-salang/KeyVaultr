# Generated by Django 4.2.1 on 2023-05-27 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccountCredentials', '0007_alter_accountcredential_encrypted_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountcredential',
            name='encrypted_password',
            field=models.BinaryField(blank=True),
        ),
    ]
