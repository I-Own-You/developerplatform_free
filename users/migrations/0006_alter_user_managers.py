# Generated by Django 3.2.9 on 2021-12-17 18:26

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
    ]
