# Generated by Django 2.0.1 on 2018-01-19 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jediteacher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jediuser',
            name='email',
            field=models.TextField(default=None),
        ),
    ]