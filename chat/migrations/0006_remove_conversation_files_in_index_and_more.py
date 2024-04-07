# Generated by Django 5.0.4 on 2024-04-07 15:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0005_conversation_files_in_index"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="conversation",
            name="files_in_index",
        ),
        migrations.AddField(
            model_name="conversation",
            name="indexed_file_ids",
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
