# Generated by Django 4.2.5 on 2023-11-29 02:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0002_author_category_comment_tag_alter_user_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='interests',
        ),
    ]
