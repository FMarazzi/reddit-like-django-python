# Generated by Django 2.1.5 on 2019-01-28 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0002_auto_20190124_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
    ]