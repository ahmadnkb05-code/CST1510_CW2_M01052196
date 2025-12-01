import bcrypt
import streamlit as st
from db_manager import DatabaseManager

st.set_page_config(page_title="Login")
st.title("Login")

db = DatabaseManager()
db.create_tables()


def verify(username: str, password: str):
    rows = db.query("SELECT password_hash, role FROM users WHERE username = ?;", (username,))
    if not rows:
        return None
    stored_hex = rows[0]["password_hash"]
    stored_hash = bytes.fromhex(stored_hex)
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
        return {"username": username, "role": rows[0]["role"]}
    return None


with st.form("login_form"):
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    ok = st.form_submit_button("Login")
    if ok:
        user = verify(u, p)
        if user:
            st.session_state["user"] = user
            st.success(f"Logged in as {user['username']} ({user['role']})")
        else:
            st.error("Invalid credentials. Tip: run auth.py then migrate_users_to_db.py")
