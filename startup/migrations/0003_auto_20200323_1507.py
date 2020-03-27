# Generated by Django 2.2.6 on 2020-03-23 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startup', '0002_auto_20200323_1421'),
    ]

    operations = [
        migrations.RenameField(
            model_name='countryperformance',
            old_name='GDP_growth',
            new_name='value',
        ),
        migrations.AddField(
            model_name='countryperformance',
            name='performance_index',
            field=models.CharField(default='Unknown', max_length=200),
            preserve_default=False,
        ),
    ]
