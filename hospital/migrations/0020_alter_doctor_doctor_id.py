# Generated by Django 3.2.15 on 2024-12-02 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0019_auto_20241126_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='doctor_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
