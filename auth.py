"""
auth.py
A cool terminal tool to:
register a user (username and password)
securely hash the password with bcrypt
store "username|hash_hex|role" lines in users.txt
Later we migrate these users into SQLite.
"""

import getpass
from pathlib import Path
import bcrypt

USERS_FILE = Path("users.txt")


def hash_password(plain: str) -> bytes:
    """Turn a plain password into a salted bcrypt hash."""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())


def verify_password(plain: str, hashed: bytes) -> bool:
    """Check a plain password against a stored bcrypt hash."""
    return bcrypt.checkpw(plain.encode("utf-8"), hashed)


def load_users_from_file():
    """Read users.txt and return {username: (hash_bytes, role)}."""
    users = {}
    if not USERS_FILE.exists():
        return users
    for line in USERS_FILE.read_text().splitlines():
        if not line.strip():
            continue
        parts = line.split("|")
        if len(parts) != 3:
            continue
        username, hash_hex, role = parts
        try:
            users[username] = (bytes.fromhex(hash_hex), role)
        except Exception:
            # ignore malformed lines
            continue
    return users


def register_user():
    print("\n---Register user please---")
    username = input("Username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    role = input("Role (cyber / it / user — press Enter for user): ").strip() or "user"
    p1 = getpass.getpass("Password: ")
    p2 = getpass.getpass("Confirm password: ")
    if p1 != p2:
        print("Passwords do not match.")
        return
    hashed = hash_password(p1)
    line = f"{username}|{hashed.hex()}|{role}\n"
    if USERS_FILE.exists():
        USERS_FILE.write_text(USERS_FILE.read_text() + line)
    else:
        USERS_FILE.write_text(line)
    print(f"✔ Registered '{username}'")


def login_user():
    print("\n=== Login ===")
    username = input("Username: ").strip()
    pwd = getpass.getpass("Password: ")
    users = load_users_from_file()
    if username not in users:
        print("No such user.")
        return None
    stored_hash, role = users[username]
    if verify_password(pwd, stored_hash):
        print(f"✔ Login OK — role: {role}")
        return {"username": username, "role": role}
    print("❌ Wrong password.")
    return None


def main():
    while True:
        print("\n[r]egister  [l]ogin  [q]uit")
        choice = input("Choice: ").strip().lower()
        if choice == "r":
            register_user()
        elif choice == "l":
            user = login_user()
            if user:
                print("You can now migrate this user to the database.")
        elif choice == "q":
            break
        else:
            print("Unknown option.")


if __name__ == "__main__":
    main()
