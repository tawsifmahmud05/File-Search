# Generated by Django 3.2.6 on 2021-11-28 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0003_alter_url_depth'),
    ]

    operations = [
        migrations.AddField(
            model_name='cluster',
            name='crawled',
            field=models.IntegerField(default=0),
        ),
    ]
