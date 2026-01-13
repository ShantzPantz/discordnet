'''
Passive plugin that silently tracks messages from @yaobviously about Claude Code.
This plugin runs in the background and does not respond to commands.
'''

import re
import config
from db import execute_query

# No command - this is a passive plugin
COMMAND = None

# Keywords to track (case-insensitive)
CLAUDE_CODE_KEYWORDS = [
    'claude code',
    'claudecode',
]

# Target username to track
TARGET_USERNAME = 'yaobviously'


async def init():
    """Initialize the database table for tracking Claude Code mentions"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS claude_code_mentions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        username TEXT NOT NULL,
        message_id TEXT NOT NULL,
        channel_id TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        message_content TEXT
    );
    """
    try:
        execute_query(config.MAIN_DATABASE, create_table_sql)
        print("Claude Code tracker initialized successfully")
    except Exception as e:
        print(f"Error initializing Claude Code tracker: {e}")


def contains_claude_code_reference(content):
    """Check if the message content contains a reference to Claude Code"""
    if not content:
        return False

    content_lower = content.lower()
    for keyword in CLAUDE_CODE_KEYWORDS:
        if keyword in content_lower:
            return True
    return False


async def main(bot, message, **kwargs):
    """
    Passively monitor messages for Claude Code references from yaobviously.
    This function runs silently and does not send any responses.
    """
    # Check if the message is from the target user
    if message.author.name.lower() != TARGET_USERNAME.lower():
        return

    # Check if the message contains Claude Code references
    if not contains_claude_code_reference(message.content):
        return

    # Log the mention to the database
    insert_sql = """
    INSERT INTO claude_code_mentions (user_id, username, message_id, channel_id, message_content)
    VALUES (?, ?, ?, ?, ?);
    """

    try:
        execute_query(
            config.MAIN_DATABASE,
            insert_sql,
            (
                str(message.author.id),
                message.author.name,
                str(message.id),
                str(message.channel.id),
                message.content[:500]  # Store first 500 chars to avoid huge text
            )
        )
        # Silent operation - no output or messages sent
    except Exception as e:
        print(f"Error tracking Claude Code mention: {e}")
