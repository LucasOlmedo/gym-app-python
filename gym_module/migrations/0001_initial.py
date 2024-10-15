# Generated by Django 5.1.2 on 2024-10-15 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_part', models.CharField(max_length=100)),
                ('equipment', models.CharField(max_length=100)),
                ('gif_url', models.CharField(max_length=100)),
                ('ref_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('target', models.CharField(max_length=100)),
                ('secondary_muscles', models.TextField()),
                ('instructions', models.TextField()),
            ],
        ),
    ]