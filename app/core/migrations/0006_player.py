# Generated by Django 4.0.3 on 2022-03-09 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_game_track_health'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.game')),
            ],
        ),
    ]
