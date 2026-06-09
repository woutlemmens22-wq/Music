import sqlite3
import requests
import time

DB = "music.db"

HEADERS = {
    "User-Agent": "MusicSchoolProject/1.0 (test@test.com)"
}

ARTIESTEN = [
("Radiohead", "Rock"),
("Joey Badass", "Hip-Hop"),





]

def get_db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def api_get(url, params=None):
    try:
        r = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=10
        )

        r.raise_for_status()
        time.sleep(1)

        return r.json()

    except requests.exceptions.RequestException as e:
        print("API fout:", e)
        return None

def zoek_artiest_id(naam):
    data = api_get(
        "https://musicbrainz.org/ws/2/artist",
        {"query": naam, "limit": 1, "fmt": "json"}
    )

    if data and data.get("artists"):
        return data["artists"][0]["id"]

    return None

def zoek_cover(release_group_id):
    try:
        r = requests.get(
            f"https://coverartarchive.org/release-group/{release_group_id}/front",
            headers=HEADERS,
            timeout=5,
            allow_redirects=True
        )

        return r.url if r.status_code == 200 else None

    except Exception:
        return None

def zoek_tracks(release_group_id):
    data = api_get(
        "https://musicbrainz.org/ws/2/release",
        {
            "release-group": release_group_id,
            "limit": 1,
            "fmt": "json"
        }
    )

    if not data or not data.get("releases"):
        return []

    release_id = data["releases"][0]["id"]

    data = api_get(
        f"https://musicbrainz.org/ws/2/release/{release_id}",
        {
            "inc": "recordings",
            "fmt": "json"
        }
    )

    if not data:
        return []

    tracks = []

    for medium in data.get("media", []):
        for track in medium.get("tracks", []):

            lengte = track.get("length")

            duur = "-"

            if lengte:
                minuten = lengte // 60000
                seconden = (lengte % 60000) // 1000
                duur = f"{minuten}:{seconden:02d}"

            tracks.append((
                track.get("position", 0),
                track.get("title", "Onbekend"),
                duur
            ))

    return tracks

def seed():

    con = get_db()

    con.commit()

    for artiest, genre in ARTIESTEN:

        print(f"\n🎵 {artiest}")

        artiest_id = zoek_artiest_id(artiest)

        if not artiest_id:
            print("Niet gevonden")
            continue

        data = api_get(
            "https://musicbrainz.org/ws/2/release-group",
            {
                "artist": artiest_id,
                "type": "album",
                "limit": 10,
                "fmt": "json"
            }
        )

        if not data:
            continue

        albums = data.get("release-groups", [])

        for i, album in enumerate(albums):

            titel = album.get("title", "Onbekend")

            jaar = album.get("first-release-date", "0")[:4]
            jaar = int(jaar) if jaar.isdigit() else 0

            release_group_id = album.get("id")

            cover = zoek_cover(release_group_id)

            print(f"  ➜ {titel}")

            cur = con.execute("""
                INSERT OR IGNORE INTO albums
                (title, artist, genre, year, price, type, cover_url, popularity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                titel,
                artiest,
                genre,
                jaar,
                round(19.99 - i, 2),
                "CD",
                cover,
                100 - (i * 10)
            ))

            album_id = cur.lastrowid

            tracks = zoek_tracks(release_group_id)

            for positie, naam, duur in tracks:
                con.execute("""
                    INSERT OR IGNORE INTO tracks
                    (album_id, position, title, duration)
                    VALUES (?, ?, ?, ?)
                """, (
                    album_id,
                    positie,
                    naam,
                    duur
                ))

            print(f"     {len(tracks)} tracks")

        con.commit()

    con.close()

    print("\n✅ Database gevuld!")

if __name__ == "__main__":
    seed()