# Generated by Django 2.0.1 on 2018-01-20 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jediteacher', '0008_auto_20180120_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlabels',
            name='mode',
            field=models.TextField(default=''),
        ),
    ]
