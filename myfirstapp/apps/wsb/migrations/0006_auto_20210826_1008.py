# Generated by Django 3.2.6 on 2021-08-26 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wsb', '0005_auto_20210826_0704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subreddit',
            name='author',
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=50, verbose_name='author name')),
                ('comment_text', models.CharField(max_length=200, verbose_name='commentary text')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wsb.author')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
    ]
