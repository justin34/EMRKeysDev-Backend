# Generated by Django 4.2.3 on 2023-07-04 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='user',
            new_name='app_user',
        ),
    ]
