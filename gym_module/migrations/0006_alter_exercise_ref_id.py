# Generated by Django 5.1.2 on 2024-10-22 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_module', '0005_remove_personalinfo_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='ref_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
