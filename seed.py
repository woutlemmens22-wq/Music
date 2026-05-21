import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


import sqlite3
import requests
import time

DB = "music.db"

ARTIESTEN = [
    ("The Beatles", "Rock"),
    ("Kendrick Lamar", "Hip-Hop"),
    ("Radiohead", "Rock"),
    ("Daft Punk", "Electronic"),
    ("Amy Winehouse", "Jazz"),
    ("Arctic Monkeys", "Rock"),
    ("Michael Jackson", "Pop"),
    ("Miles Davis", "Jazz"),
    ("Eminem", "Hip-Hop"),
    ("Pink Floyd", "Rock"),
]

HEADERS = {
    "User-Agent": "MyMusicApp/1.0 (wout@example.com)"
}

def get_db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def zoek_artiest_id(naam):
    r = requests.get(
        "https://musicbrainz.org/ws/2/artist",
        params={"query": naam, "limit": 1, "fmt": "json"},
        headers=HEADERS
        verify=False   
    )
    resultaten = r.json().get("artists", [])
    if resultaten:
        return resultaten[0]["id"]
    return None

def zoek_cover(release_group_id):
    try:
        r = requests.get(
            f"https://coverartarchive.org/release-group/{release_group_id}/front",
            headers=HEADERS,
            allow_redirects=True,
            timeout=5
            verify=False   
        )
        if r.status_code == 200:
            return r.url
    except Exception:
        pass
    return None

def zoek_tracklist(release_group_id):
    try:
        r = requests.get(
            "https://musicbrainz.org/ws/2/release",
            params={
                "release-group": release_group_id,
                "limit": 1,
                "fmt": "json"
            },
            headers=HEADERS
            verify=False   
        )
        releases = r.json().get("releases", [])
        if not releases:
            return []

        release_id = releases[0]["id"]
        time.sleep(0.5)

        r = requests.get(
            f"https://musicbrainz.org/ws/2/release/{release_id}",
            params={"inc": "recordings", "fmt": "json"},
            headers=HEADERS
            verify=False   
        )
        data = r.json()
        tracks = []
        for medium in data.get("media", []):
            for track in medium.get("tracks", []):
                titel = track.get("title", "Onbekend")
                positie = track.get("position", 0)
                lengte = track.get("length")
                if lengte:
                    minuten = lengte // 60000
                    seconden = (lengte % 60000) // 1000
                    duur = f"{minuten}:{seconden:02d}"
                else:
                    duur = "-"
                tracks.append((positie, titel, duur))
        return tracks
    except Exception:
        return []

def seed():
    con = get_db()
    con.execute("DELETE FROM albums")
    con.execute("DELETE FROM tracks")
    con.commit()

    for artiest, genre in ARTIESTEN:
        print(f"Bezig met {artiest}...")

        artiest_id = zoek_artiest_id(artiest)
        if not artiest_id:
            print(f"  Niet gevonden: {artiest}")
            time.sleep(1.2)
            continue

        time.sleep(1.2)

        r = requests.get(
            "https://musicbrainz.org/ws/2/release-group",
            params={
                "artist": artiest_id,
                "type": "album",
                "limit": 5,
                "fmt": "json"
            },
            headers=HEADERS
        )

        albums = r.json().get("release-groups", [])
        print(f"  {len(albums)} albums gevonden")

        for i, album in enumerate(albums):
            titel = album.get("title", "Onbekend")
            jaar = album.get("first-release-date", "0")[:4]
            jaar = int(jaar) if jaar.isdigit() else 0
            populariteit = 100 - (i * 15)
            release_group_id = album.get("id")

            cover = zoek_cover(release_group_id)
            print(f"    - {titel} | cover: {'ja' if cover else 'nee'}")

            con.execute("""
                INSERT INTO albums (title, artist, genre, year, price, type, cover_url, popularity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (titel, artiest, genre, jaar, round(19.99 - i, 2), "cd", cover, populariteit))
            con.commit()

            album_row = con.execute(
                "SELECT id FROM albums WHERE title=? AND artist=?", (titel, artiest)
            ).fetchone()

            if album_row:
                tracks = zoek_tracklist(release_group_id)
                for positie, track_titel, duur in tracks:
                    con.execute("""
                        INSERT INTO tracks (album_id, position, title, duration)
                        VALUES (?, ?, ?, ?)
                    """, (album_row["id"], positie, track_titel, duur))
                con.commit()
                print(f"      {len(tracks)} nummers toegevoegd")

            time.sleep(1.2)

        time.sleep(1.2)

    con.close()
    print("✅ Database gevuld!")

if __name__ == "__main__":
    seed()