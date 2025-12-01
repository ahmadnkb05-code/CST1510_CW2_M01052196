"""
migrate_users_to_db.py
Reads users from users.txt and inserts them into the SQLite users table.
Run this after you register at least one user with auth.py.
"""

from auth import load_users_from_file
from models import insert_user
from db_manager import DatabaseManager


def migrate():
    db = DatabaseManager()
    db.create_tables()
    users = load_users_from_file()
    for username, (hash_bytes, role) in users.items():
        insert_user(username, hash_bytes.hex(), role)
    print("✔ Migration complete.")


if __name__ == "__main__":
    migrate()
