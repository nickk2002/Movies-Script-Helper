# Generated by Django 2.0.7 on 2021-03-27 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0004_auto_20210325_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='background_path',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
