# Generated by Django 4.0.3 on 2022-03-08 21:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_game'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='ownder',
            new_name='owner',
        ),
    ]