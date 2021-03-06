# Generated by Django 3.1.1 on 2020-09-05 08:11

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_comment_sentiments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='timestamp',
            field=models.DateField(default=datetime.datetime(2020, 9, 5, 8, 11, 42, 272139, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='comments.product'),
        ),
    ]
