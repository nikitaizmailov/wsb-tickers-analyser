# Generated by Django 3.2.6 on 2021-08-29 12:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wsb', '0011_alter_comment_subreddit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subreddit',
            name='post_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Published'),
        ),
        migrations.AlterField(
            model_name='subreddit',
            name='submission_title',
            field=models.CharField(max_length=500, verbose_name='Submission Title'),
        ),
    ]
