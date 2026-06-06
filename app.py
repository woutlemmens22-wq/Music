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
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            voornaam TEXT,
            achternaam TEXT,
            straat TEXT,
            huisnummer TEXT,
            postcode TEXT,
            stad TEXT,
            land TEXT,
            totaal REAL,
            datum TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)
    con.commit()
    con.close()

@app.route("/")
def index():
    con = get_db()
    albums = con.execute("""
        SELECT * FROM albums 
        ORDER BY 
            CASE WHEN cover_url IS NOT NULL THEN 0 ELSE 1 END,
            popularity DESC
    """).fetchall()
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
    albums = con.execute("""
        SELECT * FROM albums 
        WHERE genre = ?
        ORDER BY 
            CASE WHEN cover_url IS NOT NULL THEN 0 ELSE 1 END,
            popularity DESC
    """, (genre,)).fetchall()
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
            session["is_admin"] = user["is_admin"]
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
    referrer = request.referrer
    if referrer:
        return redirect(referrer + "#album-" + str(album_id))
    return redirect("/")

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
    totaal = sum(item["price"] * item["quantity"] for item in items)
    session["cart_count"] = sum(item["quantity"] for item in items)
    return render_template("cart.html", items=items, totaal=totaal)

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
    count = con.execute(
        "SELECT SUM(quantity) FROM cart WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()[0]
    con.close()
    session["cart_count"] = count or 0
    flash("Album toegevoegd aan je winkelwagen!", "success")
    return redirect(request.referrer or "/")

@app.route("/cart/update/<int:album_id>", methods=["POST"])
def cart_update(album_id):
    if "user_id" not in session:
        return redirect("/login")
    quantity = int(request.form["quantity"])
    if quantity < 1:
        quantity = 1
    if quantity > 99:
        quantity = 99
    con = get_db()
    con.execute(
        "UPDATE cart SET quantity = ? WHERE user_id = ? AND album_id = ?",
        (quantity, session["user_id"], album_id)
    )
    con.commit()
    count = con.execute(
        "SELECT SUM(quantity) FROM cart WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()[0]
    con.close()
    session["cart_count"] = count or 0
    return redirect("/cart")

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
    count = con.execute(
        "SELECT SUM(quantity) FROM cart WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()[0]
    con.close()
    session["cart_count"] = count or 0
    flash("Album verwijderd uit je winkelwagen.", "success")
    return redirect("/cart")

@app.route("/zoek")
def zoek():
    q = request.args.get("q", "")
    con = get_db()
    albums = con.execute(
        "SELECT * FROM albums WHERE LOWER(title) LIKE LOWER(?) OR LOWER(artist) LIKE LOWER(?) ORDER BY popularity DESC",
        (f"%{q}%", f"%{q}%")
    ).fetchall()
    con.close()
    return render_template("zoek.html", albums=albums, q=q)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if "user_id" not in session:
        return redirect("/login")
    con = get_db()
    items = con.execute("""
        SELECT albums.*, cart.quantity FROM albums
        JOIN cart ON albums.id = cart.album_id
        WHERE cart.user_id = ?
    """, (session["user_id"],)).fetchall()
    if not items:
        flash("Je winkelwagen is leeg!", "danger")
        return redirect("/cart")
    if request.method == "POST":
        voornaam = request.form["voornaam"]
        achternaam = request.form["achternaam"]
        straat = request.form["straat"]
        huisnummer = request.form["huisnummer"]
        postcode = request.form["postcode"]
        stad = request.form["stad"]
        land = request.form["land"]
        if not voornaam or not achternaam or not straat or not huisnummer or not postcode or not stad:
            flash("Vul alle velden in.", "danger")
            return render_template("checkout.html", items=items)
        totaal = sum(item["price"] * item["quantity"] for item in items)
        from datetime import datetime
        datum = datetime.now().strftime("%d/%m/%Y %H:%M")
        con.execute("""
            INSERT INTO orders (user_id, username, voornaam, achternaam, straat, huisnummer, postcode, stad, land, totaal, datum)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (session["user_id"], session["username"], voornaam, achternaam, straat, huisnummer, postcode, stad, land, totaal, datum))
        con.execute("DELETE FROM cart WHERE user_id = ?", (session["user_id"],))
        con.commit()
        con.close()
        session["cart_count"] = 0
        flash(f"Bestelling geplaatst! Je pakket wordt verstuurd naar {straat} {huisnummer}, {postcode} {stad}.", "success")
        return redirect("/")
    con.close()
    totaal = sum(item["price"] * item["quantity"] for item in items)
    return render_template("checkout.html", items=items, totaal=totaal)

@app.route("/admin/orders")
def admin_orders():
    if "user_id" not in session or not session.get("is_admin"):
        return redirect("/")
    con = get_db()
    orders = con.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    con.close()
    return render_template("admin_orders.html", orders=orders)

@app.route("/admin/orders/delete/<int:order_id>")
def admin_orders_delete(order_id):
    if "user_id" not in session or not session.get("is_admin"):
        return redirect("/")
    con = get_db()
    con.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    con.commit()
    con.close()
    flash("Bestelling verwijderd.", "success")
    return redirect("/admin/orders")

@app.route("/admin/orders/add", methods=["GET", "POST"])
def admin_orders_add():
    if "user_id" not in session or not session.get("is_admin"):
        return redirect("/")
    if request.method == "POST":
        from datetime import datetime
        voornaam = request.form["voornaam"]
        achternaam = request.form["achternaam"]
        straat = request.form["straat"]
        huisnummer = request.form["huisnummer"]
        postcode = request.form["postcode"]
        stad = request.form["stad"]
        land = request.form["land"]
        totaal = request.form["totaal"]
        datum = datetime.now().strftime("%d/%m/%Y %H:%M")
        con = get_db()
        con.execute("""
            INSERT INTO orders (user_id, username, voornaam, achternaam, straat, huisnummer, postcode, stad, land, totaal, datum)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (session["user_id"], session["username"], voornaam, achternaam, straat, huisnummer, postcode, stad, land, totaal, datum))
        con.commit()
        con.close()
        flash("Bestelling toegevoegd!", "success")
        return redirect("/admin/orders")
    return render_template("admin_orders_add.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)