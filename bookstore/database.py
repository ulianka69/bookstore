from pathlib import Path
import mysql.connector
from mysql.connector import pooling
import config

IMAGES_DIR = Path(__file__).parent / "images"
COVERS_DIR = IMAGES_DIR / "covers"
AUTHORS_DIR = IMAGES_DIR / "authors"
COVERS_DIR.mkdir(parents=True, exist_ok=True)
AUTHORS_DIR.mkdir(parents=True, exist_ok=True)

import codecs
codecs.register(lambda name: codecs.lookup("utf8") if name == "utf8mb4" else None)

_pool = pooling.MySQLConnectionPool(
    pool_name="bookstore_pool",
    pool_size=5,
    pool_reset_session=True,
    **config.MYSQL_CONFIG,
)


def get_connection():
    return _pool.get_connection()


def init_db():
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(64) UNIQUE NOT NULL,
                password_hash VARCHAR(128) NOT NULL,
                role ENUM('admin','user') DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS authors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                photo_path VARCHAR(512) NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS genres (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(128) UNIQUE NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10,2) DEFAULT 0,
                year INT NULL,
                cover_path VARCHAR(512) NULL,
                genre_id INT NULL,
                stock INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS book_authors (
                book_id INT NOT NULL,
                author_id INT NOT NULL,
                PRIMARY KEY (book_id, author_id),
                FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
                FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        con.commit()

        import bcrypt
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            hashed = bcrypt.hashpw("admin".encode(), bcrypt.gensalt()).decode()
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, 'admin')",
                ("admin", hashed),
            )
        cur.execute("SELECT COUNT(*) FROM genres")
        if cur.fetchone()[0] == 0:
            cur.executemany(
                "INSERT INTO genres (name) VALUES (%s)",
                [("Фантастика",), ("Детектив",), ("Роман",),
                 ("Фэнтези",), ("Наука",)],
            )
        con.commit()
    finally:
        cur.close()
        con.close()