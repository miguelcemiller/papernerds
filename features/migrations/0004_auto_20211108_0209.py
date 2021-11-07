# Generated by Django 3.2.7 on 2021-11-07 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0003_portal'),
    ]

    operations = [
        migrations.AddField(
            model_name='portal',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='portal',
            name='step',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
