# Generated by Django 3.2.6 on 2021-12-05 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0012_alter_file_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='mainurl',
            field=models.IntegerField(default=0),
        ),
    ]
