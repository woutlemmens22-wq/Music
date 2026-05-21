from flask import render_template, redirect, flash, request, session
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "geheime_sleutel"

DB = "music.db"

def get_db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = get_db()
    con.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            genre TEXT NOT NULL,
            year INTEGER,
            price REAL,
            type TEXT,
            cover_url TEXT,
            popularity INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            album_id INTEGER,
            position INTEGER,
            title TEXT,
            duration TEXT,
            FOREIGN KEY(album_id) REFERENCES albums(id)
        );
        CREATE TABLE IF NOT EXISTS wishlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            album_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(album_id) REFERENCES albums(id)
        );
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            album_id INTEGER,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(album_id) REFERENCES albums(id)
        );
    """)
    con.commit()
    con.close()

@app.route("/")
def index():
    con = get_db()
    albums = con.execute("SELECT * FROM albums WHERE cover_url IS NOT NULL ORDER BY popularity DESC").fetchall()
    con.close()
    return render_template("index.html", albums=albums)

@app.route("/album/<int:album_id>")
def album(album_id):
    con = get_db()
    album = con.execute("SELECT * FROM albums WHERE id = ?", (album_id,)).fetchone()
    tracks = con.execute("SELECT * FROM tracks WHERE album_id = ? ORDER BY position", (album_id,)).fetchall()
    con.close()
    return render_template("album.html", album=album, tracks=tracks)

@app.route("/genre/<genre>")
def genre_pagina(genre):
    con = get_db()
    albums = con.execute(
        "SELECT * FROM albums WHERE genre = ? ORDER BY popularity DESC",
        (genre,)
    ).fetchall()
    con.close()
    return render_template("genre.html", genre=genre, albums=albums)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        try:
            con = get_db()
            con.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            con.commit()
            con.close()
            flash("Account aangemaakt! Je kan nu inloggen.", "success")
            return redirect("/login")
        except:
            flash("Gebruikersnaam al in gebruik.", "danger")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        con = get_db()
        user = con.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        con.close()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash(f"Welkom terug, {username}!", "success")
            return redirect("/")
        flash("Verkeerde gebruikersnaam of wachtwoord.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/wishlist")
def wishlist():
    if "user_id" not in session:
        return redirect("/login")
    con = get_db()
    albums = con.execute("""
        SELECT albums.* FROM albums
        JOIN wishlist ON albums.id = wishlist.album_id
        WHERE wishlist.user_id = ?
    """, (session["user_id"],)).fetchall()
    con.close()
    return render_template("wishlist.html", albums=albums)

@app.route("/wishlist/add/<int:album_id>")
def wishlist_add(album_id):
    if "user_id" not in session:
        return redirect("/login")
    con = get_db()
    con.execute(
        "INSERT OR IGNORE INTO wishlist (user_id, album_id) VALUES (?, ?)",
        (session["user_id"], album_id)
    )
    con.commit()
    con.close()
    flash("Album toegevoegd aan je wishlist!", "success")
    return redirect(request.referrer or "/")

@app.route("/wishlist/remove/<int:album_id>")
def wishlist_remove(album_id):
    if "user_id" not in session:
        return redirect("/login")
    con = get_db()
    con.execute(
        "DELETE FROM wishlist WHERE user_id = ? AND album_id = ?",
        (session["user_id"], album_id)
    )
    con.commit()
    con.close()
    flash("Album verwijderd uit je wishlist.", "success")
    return redirect("/wishlist")

@app.route("/cart")
def cart():
    if "user_id" not in session:
        return redirect("/login")
    con = get_db()
    items = con.execute("""
        SELECT albums.*, cart.quantity FROM albums
        JOIN cart ON albums.id = cart.album_id
        WHERE cart.user_id = ?
    """, (session["user_id"],)).fetchall()
    con.close()
    return render_template("cart.html", items=items)

@app.route("/cart/add/<int:album_id>")
def cart_add(album_id):
    if "user_id" not in session:
        return redirect("/login")
    con = get_db()
    con.execute(
        "INSERT OR IGNORE INTO cart (user_id, album_id) VALUES (?, ?)",
        (session["user_id"], album_id)
    )
    con.commit()
    con.close()
    flash("Album toegevoegd aan je winkelwagen!", "success")
    return redirect(request.referrer or "/")

@app.route("/cart/remove/<int:album_id>")
def cart_remove(album_id):
    if "user_id" not in session:
        return redirect("/login")
    con = get_db()
    con.execute(
        "DELETE FROM cart WHERE user_id = ? AND album_id = ?",
        (session["user_id"], album_id)
    )
    con.commit()
    con.close()
    flash("Album verwijderd uit je winkelwagen.", "success")
    return redirect("/cart")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)