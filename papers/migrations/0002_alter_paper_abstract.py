# Generated by Django 3.2.7 on 2021-10-08 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='abstract',
            field=models.TextField(blank=True, null=True),
        ),
    ]