"""Migrations for chat model."""

from django.db import migrations


class Migration(migrations.Migration):
    """Migrations for Chat app to alter model options and table names."""

    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="chat",
            options={"verbose_name": "Chats", "verbose_name_plural": "Chats"},
        ),
        migrations.AlterModelOptions(
            name="chatmessage",
            options={
                "verbose_name": "Chat_messages",
                "verbose_name_plural": "Chat_messages",
            },
        ),
        migrations.AlterModelTable(
            name="chat",
            table="chats",
        ),
        migrations.AlterModelTable(
            name="chatmessage",
            table="chat_messages",
        ),
    ]
