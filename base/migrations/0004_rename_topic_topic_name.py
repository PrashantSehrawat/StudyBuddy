# Generated by Django 4.2.2 on 2023-06-14 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_room_options_rename_topic_room_topic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='topic',
            new_name='name',
        ),
    ]