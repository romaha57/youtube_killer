# Generated by Django 4.2.2 on 2023-06-15 08:32

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('app_channel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='верицицирован'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='keywords',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='теги канала'),
        ),
    ]