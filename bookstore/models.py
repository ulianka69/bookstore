import shutil
from pathlib import Path
from database import get_connection, COVERS_DIR, AUTHORS_DIR


def _copy_image(src, dest_dir):
    src_path = Path(src)
    dest = dest_dir / src_path.name
    i = 1
    while dest.exists() and dest.resolve() != src_path.resolve():
        dest = dest_dir / f"{src_path.stem}_{i}{src_path.suffix}"
        i += 1
    if dest.resolve() != src_path.resolve():
        shutil.copy(src_path, dest)
    return str(dest.relative_to(dest_dir.parent.parent))


def get_genres():
    con = get_connection(); cur = con.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM genres ORDER BY name")
        return cur.fetchall()
    finally:
        cur.close(); con.close()


def add_genre(name):
    con = get_connection(); cur = con.cursor()
    try:
        cur.execute("INSERT INTO genres (name) VALUES (%s)", (name,))
        con.commit()
    finally:
        cur.close(); con.close()


def delete_genre(genre_id):
    con = get_connection(); cur = con.cursor()
    try:
        cur.execute("DELETE FROM genres WHERE id=%s", (genre_id,))
        con.commit()
    finally:
        cur.close(); con.close()


def get_authors():
    con = get_connection(); cur = con.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM authors ORDER BY full_name")
        return cur.fetchall()
    finally:
        cur.close(); con.close()


def add_author(full_name, photo_src=None):
    photo_path = _copy_image(photo_src, AUTHORS_DIR) if photo_src else None
    con = get_connection(); cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO authors (full_name, photo_path) VALUES (%s, %s)",
            (full_name, photo_path),
        )
        con.commit()
    finally:
        cur.close(); con.close()


def update_author(author_id, full_name, photo_src=None):
    con = get_connection(); cur = con.cursor()
    try:
        if photo_src:
            photo_path = _copy_image(photo_src, AUTHORS_DIR)
            cur.execute(
                "UPDATE authors SET full_name=%s, photo_path=%s WHERE id=%s",
                (full_name, photo_path, author_id),
            )
        else:
            cur.execute(
                "UPDATE authors SET full_name=%s WHERE id=%s",
                (full_name, author_id),
            )
        con.commit()
    finally:
        cur.close(); con.close()


def delete_author(author_id):
    con = get_connection(); cur = con.cursor()
    try:
        cur.execute("DELETE FROM authors WHERE id=%s", (author_id,))
        con.commit()
    finally:
        cur.close(); con.close()


def get_books(query="", genre_id=None, sort_by="title", order="ASC"):
    allowed = {"title", "year", "price", "created_at", "stock"}
    sort_by = sort_by if sort_by in allowed else "title"
    order = "ASC" if order.upper() == "ASC" else "DESC"

    sql = f"""
        SELECT b.*, g.name AS genre_name
        FROM books b
        LEFT JOIN genres g ON g.id = b.genre_id
        WHERE (b.title LIKE %s OR IFNULL(b.description,'') LIKE %s)
    """
    params = [f"%{query}%", f"%{query}%"]
    if genre_id:
        sql += " AND b.genre_id = %s"
        params.append(genre_id)
    sql += f" ORDER BY b.{sort_by} {order}"

    con = get_connection(); cur = con.cursor(dictionary=True)
    try:
        cur.execute(sql, params)
        books = cur.fetchall()
        for b in books:
            cur.execute("""
                SELECT a.full_name
                FROM book_authors ba
                JOIN authors a ON a.id = ba.author_id
                WHERE ba.book_id = %s
                ORDER BY a.full_name
            """, (b["id"],))
            rows = cur.fetchall()
            b["authors"] = ", ".join(r["full_name"] for r in rows) if rows else None
        return books
    finally:
        cur.close(); con.close()


def get_book(book_id):
    con = get_connection(); cur = con.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM books WHERE id=%s", (book_id,))
        return cur.fetchone()
    finally:
        cur.close(); con.close()


def get_book_author_ids(book_id):
    con = get_connection(); cur = con.cursor()
    try:
        cur.execute("SELECT author_id FROM book_authors WHERE book_id=%s", (book_id,))
        return [row[0] for row in cur.fetchall()]
    finally:
        cur.close(); con.close()


def add_book(title, description, price, year, genre_id, stock,
             cover_src=None, author_ids=None):
    cover_path = _copy_image(cover_src, COVERS_DIR) if cover_src else None
    con = get_connection(); cur = con.cursor()
    try:
        cur.execute(
            """INSERT INTO books
               (title, description, price, year, genre_id, stock, cover_path)
               VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            (title, description, price, year, genre_id, stock, cover_path),
        )
        book_id = cur.lastrowid
        for a_id in (author_ids or []):
            cur.execute(
                "INSERT IGNORE INTO book_authors (book_id, author_id) VALUES (%s,%s)",
                (book_id, a_id),
            )
        con.commit()
        return book_id
    finally:
        cur.close(); con.close()


def update_book(book_id, title, description, price, year, genre_id, stock,
                cover_src=None, author_ids=None):
    con = get_connection(); cur = con.cursor()
    try:
        if cover_src:
            cover_path = _copy_image(cover_src, COVERS_DIR)
            cur.execute(
                """UPDATE books SET title=%s, description=%s, price=%s, year=%s,
                   genre_id=%s, stock=%s, cover_path=%s WHERE id=%s""",
                (title, description, price, year, genre_id, stock, cover_path, book_id),
            )
        else:
            cur.execute(
                """UPDATE books SET title=%s, description=%s, price=%s, year=%s,
                   genre_id=%s, stock=%s WHERE id=%s""",
                (title, description, price, year, genre_id, stock, book_id),
            )
        cur.execute("DELETE FROM book_authors WHERE book_id=%s", (book_id,))
        for a_id in (author_ids or []):
            cur.execute(
                "INSERT INTO book_authors (book_id, author_id) VALUES (%s,%s)",
                (book_id, a_id),
            )
        con.commit()
    finally:
        cur.close(); con.close()


def delete_book(book_id):
    con = get_connection(); cur = con.cursor()
    try:
        cur.execute("DELETE FROM books WHERE id=%s", (book_id,))
        con.commit()
    finally:
        cur.close(); con.close()