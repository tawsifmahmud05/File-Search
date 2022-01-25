# Generated by Django 3.2.6 on 2021-11-29 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0007_rename_filetype_file_filetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='crawling_strategy',
            field=models.CharField(choices=[('ALL', 'ALL'), ('DOC', 'DOC'), ('PDF', 'PDF'), ('PPT', 'PPT'), ('HTML', 'HTML')], max_length=100),
        ),
    ]
