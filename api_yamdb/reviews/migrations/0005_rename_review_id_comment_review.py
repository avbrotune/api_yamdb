# Generated by Django 3.2 on 2023-03-06 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20230306_1249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='review_id',
            new_name='review',
        ),
    ]
