# Generated by Django 3.2 on 2021-12-19 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_post_postlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='postLink',
            field=models.URLField(blank=True, max_length=255),
        ),
    ]
