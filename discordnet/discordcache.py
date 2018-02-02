import db
from sqlite3 import Error

import config


def create_messages_table():
    try:
        db.execute_query(config.MAIN_DATABASE,
           '''CREATE TABLE IF NOT EXISTS messages(
                            id BIGINT PRIMARY KEY, 
                            message_id TEXT,
                            user_id TEXT,
                            channel_id TEXT,
                            server_id TEXT,
                            user_name TEXT,
                            edited_timestamp DATETIME,
                            timestamp DATETIME,
                            tts BOOLEAN,
                            content TEXT,
                            clean_content TEXT,
                            system_content TEXT
                            )''')
    except Error as e:
        print(e)


def add_messages_to_db(m):
    sql = '''INSERT INTO messages(message_id, user_id, channel_id, server_id, user_name,
            edited_timestamp, timestamp, tts, content, clean_content, system_content)
            VALUES(?,?,?,?,?,?,?,?,?,?,?)'''

    values = (m.id, m.author.id, m.channel.id, m.server.id, m.author.name,
                m.edited_timestamp, m.timestamp, (m.tts), m.content,
                m.clean_content, m.system_content)

    print(values)
    db.execute_query(config.MAIN_DATABASE, sql, values)


def get_messages_for_user(userid):
    sql = '''SELECT * FROM messages LIMIT WHERE user_id=?'''
    results = db.execute_query(config.MAIN_DATABASE, sql, userid)
    return results


def main():
    create_messages_table()
