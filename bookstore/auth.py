import bcrypt
from database import get_connection


def register(username, password):
    username = username.strip()
    if len(username) < 3:
        return False, "Логин минимум 3 символа"
    if len(password) < 4:
        return False, "Пароль минимум 4 символа"

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    con = get_connection(); cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed),
        )
        con.commit()
        return True, "Регистрация успешна"
    except Exception:
        return False, "Такой логин уже существует"
    finally:
        cur.close(); con.close()


def login(username, password):
    con = get_connection(); cur = con.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT id, username, password_hash, role FROM users WHERE username=%s",
            (username.strip(),),
        )
        row = cur.fetchone()
        if not row:
            return None
        if bcrypt.checkpw(password.encode(), row["password_hash"].encode()):
            return {"id": row["id"], "username": row["username"], "role": row["role"]}
        return None
    finally:
        cur.close(); con.close()