import sqlite3

con = sqlite3.connect("music.db")

con.executescript("""
    CREATE TABLE IF NOT EXISTS albums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist TEXT NOT NULL,
        genre TEXT NOT NULL,
        year INTEGER,
        price REAL,
        type TEXT,
        cover_url TEXT,
        popularity INTEGER DEFAULT 0,
        UNIQUE(title, artist)
    );

    INSERT OR IGNORE INTO albums (title, artist, genre, year, price, type, cover_url, popularity) VALUES
    ('A Rush of Blood to the Head', 'Coldplay', 'Rock', 2002, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/f/f6/Coldplay_-_A_Rush_of_Blood_to_the_Head.png', 80),
    ('Ghost Stories', 'Coldplay', 'Rock', 2014, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/6/60/Coldplay_-_Ghost_Stories.png', 75),
    ('Room on Fire', 'The Strokes', 'Rock', 2003, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/c/c5/Room_on_Fire.jpg', 74),
    ('First Impressions of Earth', 'The Strokes', 'Rock', 2006, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/8/8e/First_Impressions_of_Earth.png', 73),
    ('Tranquility Base Hotel', 'Arctic Monkeys', 'Rock', 2018, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/4/4b/Tranquility_Base_Hotel_%2B_Casino.png', 72),
    ('Humbug', 'Arctic Monkeys', 'Rock', 2009, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/0/0c/Arctic_Monkeys_-_Humbug.png', 71),
    ('Pablo Honey', 'Radiohead', 'Rock', 1993, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/a/a9/Pablo_Honey.png', 70),
    ('The Bends', 'Radiohead', 'Rock', 1995, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/7/74/Radiohead.thebends.albumart.jpg', 69),
    ('Kid A', 'Radiohead', 'Electronic', 2000, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b5/Radiohead_-_Kid_A.png', 68),
    ('Amnesiac', 'Radiohead', 'Electronic', 2001, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/0/05/Radiohead_-_Amnesiac_cover.png', 67),
    ('The Number of the Beast', 'Iron Maiden', 'Metal', 1982, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/8/8b/Iron_Maiden_-_The_Number_of_the_Beast.jpg', 66),
    ('Piece of Mind', 'Iron Maiden', 'Metal', 1983, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/4/4e/Iron_Maiden_-_Piece_of_Mind.jpg', 65),
    ('Rust in Peace', 'Megadeth', 'Metal', 1990, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/5/5c/Megadeth-RustInPeace.jpg', 64),
    ('Countdown to Extinction', 'Megadeth', 'Metal', 1992, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/1/1f/Megadeth-CountdownToExtinction.jpg', 63),
    ('Ride the Lightning', 'Metallica', 'Metal', 1984, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/f/f4/Metallica_-_Ride_the_Lightning.jpg', 62),
    ('And Justice for All', 'Metallica', 'Metal', 1988, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/2/2f/Metallica_-_...And_Justice_for_All_cover.jpg', 61),
    ('Vol. 3', 'Slipknot', 'Metal', 2004, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/6/6f/Slipknot_-_Vol._3_%28The_Subliminal_Verses%29.jpg', 60),
    ('All Hope Is Gone', 'Slipknot', 'Metal', 2008, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/3/37/Slipknot_-_All_Hope_Is_Gone.jpg', 59),
    ('Nevermind', 'Soundgarden', 'Metal', 1994, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/d/d2/Soundgarden_superunknown.jpg', 58),
    ('Dirt', 'Alice in Chains', 'Metal', 1992, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/a/a9/Alice_in_Chains_-_Dirt_cover.jpg', 57),
    ('Vs.', 'Pearl Jam', 'Rock', 1993, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b1/PearlJamVs.jpg', 56),
    ('Ten', 'Pearl Jam', 'Rock', 1991, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/8/8f/Pearl_Jam_-_Ten.png', 55),
    ('Siamese Dream', 'Smashing Pumpkins', 'Rock', 1993, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/d/d3/Siamese_Dream_album_cover.jpg', 54),
    ('Mellon Collie', 'Smashing Pumpkins', 'Rock', 1995, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/0/09/Mellon_Collie_and_the_Infinite_Sadness.png', 53),
    ('Songs of Innocence', 'U2', 'Rock', 2014, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/8/8a/U2_-_Songs_of_Innocence.png', 52),
    ('Achtung Baby', 'U2', 'Rock', 1991, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/0/08/Achtung_Baby_cover.jpg', 51),
    ('Automatic for the People', 'R.E.M.', 'Rock', 1992, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/2/25/AutomaticForThePeople.jpg', 50),
    ('Out of Time', 'R.E.M.', 'Rock', 1991, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/5/52/REMOutofTime.jpg', 49),
    ('Debut', 'Bjork', 'Electronic', 1993, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/9/9e/Bjork-debut.png', 48),
    ('Post', 'Bjork', 'Electronic', 1995, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b8/Bjork-post.png', 47),
    ('Screamadelica', 'Primal Scream', 'Electronic', 1991, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/f/f2/ScreamadelicaLP.jpg', 46),
    ('Dig Your Own Hole', 'The Chemical Brothers', 'Electronic', 1997, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/f/f2/ChemBrosDYOH.jpg', 45),
    ('Exit Planet Dust', 'The Chemical Brothers', 'Electronic', 1995, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b4/The_Chemical_Brothers_-_Exit_Planet_Dust.png', 44),
    ('Fat of the Land', 'Prodigy', 'Electronic', 1997, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/9/9a/Prodigy_-_The_Fat_of_the_Land.png', 43),
    ('Music for the Jilted Generation', 'Prodigy', 'Electronic', 1994, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/5/57/Prodigy_-_Music_for_the_Jilted_Generation.png', 42),
    ('Fever', 'Kylie Minogue', 'Pop', 2001, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/3/thirty/Kylie_Minogue_-_Fever.png', 41),
    ('Justified', 'Justin Timberlake', 'Pop', 2002, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/5/fifty/Justin_Timberlake_-_Justified.png', 40),
    ('FutureSex', 'Justin Timberlake', 'Pop', 2006, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/4/4e/Justin_Timberlake_-_FutureSex_LoveSounds.png', 39),
    ('Crazy in Love', 'Beyonce', 'Pop', 2003, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/6/60/Beyonce_-_Dangerously_in_Love.png', 38),
    ('B Day', 'Beyonce', 'Pop', 2006, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/e/e9/BeyonceB%27DayAlbum.png', 37),
    ('reputation', 'Taylor Swift', 'Pop', 2017, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/9/9e/Taylor_Swift_-_Reputation.png', 36),
    ('Speak Now', 'Taylor Swift', 'Pop', 2010, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/3/thirty/Taylor_Swift_-_Speak_Now.png', 35),
    ('Midnight', 'Taylor Swift', 'Pop', 2022, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/9/9f/Midnights_by_Taylor_Swift.png', 34),
    ('Equals', 'Ed Sheeran', 'Pop', 2021, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b0/Ed_Sheeran_-_%3D_%28Equals%29.png', 33),
    ('Plus', 'Ed Sheeran', 'Pop', 2011, 15.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/d/d3/Ed_Sheeran_-_Plus.png', 32),
    ('Swimming', 'Mac Miller', 'Hip-Hop', 2018, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/9/9d/Mac_Miller_-_Swimming.png', 31),
    ('Circles', 'Mac Miller', 'Hip-Hop', 2020, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/a/a0/Mac_Miller_-_Circles.png', 30),
    ('Igor', 'Tyler the Creator', 'Hip-Hop', 2019, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/8/8e/Tyler%2C_the_Creator_-_Igor.png', 29),
    ('Flower Boy', 'Tyler the Creator', 'Hip-Hop', 2017, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/c/c9/Scum_Fuck_Flower_Boy.jpg', 28),
    ('Channel Orange', 'Frank Ocean', 'Hip-Hop', 2012, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/2/28/Channel_ORANGE.jpg', 27);
""")

con.commit()
con.close()
print("✅ 50 nieuwe albums toegevoegd!")