# Generated by Django 3.2.6 on 2021-12-20 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0015_file_filecluster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='crawling_strategy',
            field=models.CharField(choices=[('ALL', 'ALL'), ('DOC', 'DOC'), ('PDF', 'PDF'), ('PPT', 'PPT'), ('HTML', 'HTML'), ('NON-HTML', 'NON-HTML')], max_length=100),
        ),
    ]
