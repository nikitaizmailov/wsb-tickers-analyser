# Generated by Django 3.2.6 on 2021-08-26 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsb', '0010_comment_subreddit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='subreddit',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comment_set', to='wsb.subreddit'),
        ),
    ]
