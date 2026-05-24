import sqlite3


def save_log(user_msg, bot_msg):
    with sqlite3.connect("chat_logs.db") as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT,
                bot_message TEXT
            )
            """
        )

        cursor.execute(
            "INSERT INTO chat_logs (user_message, bot_message) VALUES (?, ?)",
            (user_msg, bot_msg),
        )

        conn.commit()