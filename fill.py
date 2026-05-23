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
    ('Thriller', 'Michael Jackson', 'Pop', 1982, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/5/55/Michael_Jackson_-_Thriller.png', 100),
    ('Back in Black', 'AC/DC', 'Rock', 1980, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/commons/9/92/ACDC_Back-in-Black.jpg', 99),
    ('The Dark Side of the Moon', 'Pink Floyd', 'Rock', 1973, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/3/3b/Dark_Side_of_the_Moon.png', 98),
    ('Bat Out of Hell', 'Meat Loaf', 'Rock', 1977, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/c/c1/Bat_out_of_hell.jpg', 97),
    ('Their Greatest Hits', 'Eagles', 'Rock', 1976, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/a/a0/Eagles_-_Their_Greatest_Hits_%281971-1975%29.jpg', 96),
    ('Rumours', 'Fleetwood Mac', 'Rock', 1977, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/f/fb/FMacRumours.PNG', 95),
    ('Saturday Night Fever', 'Bee Gees', 'Pop', 1977, 18.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/f/f0/Saturdaynightfever.jpg', 94),
    ('Rumours', 'Fleetwood Mac', 'Rock', 1977, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/f/fb/FMacRumours.PNG', 95),
    ('Led Zeppelin IV', 'Led Zeppelin', 'Rock', 1971, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/2/26/Led_Zeppelin_-_Led_Zeppelin_IV.jpg', 93),
    ('The Wall', 'Pink Floyd', 'Rock', 1979, 18.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/7/70/PinkFloydTheWallalbumcover.jpg', 92),
    ('Brothers in Arms', 'Dire Straits', 'Rock', 1985, 18.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/0/0e/BrothersInArms.jpg', 91),
    ('Bad', 'Michael Jackson', 'Pop', 1987, 18.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/5/51/Michael_Jackson_-_Bad.png', 90),
    ('Nevermind', 'Nirvana', 'Rock', 1991, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b7/NirvanaNevermindalbumcover.jpg', 89),
    ('Abbey Road', 'The Beatles', 'Rock', 1969, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/4/42/Beatles_-_Abbey_Road.jpg', 88),
    ('Born in the USA', 'Bruce Springsteen', 'Rock', 1984, 18.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/4/40/Born_in_the_USA.jpg', 87),
    ('Purple Rain', 'Prince', 'Pop', 1984, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/9/9c/Purplerain.jpg', 86),
    ('Appetite for Destruction', 'Guns N Roses', 'Rock', 1987, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/6/60/GunsnRosesAppetiteforDestructionalbumcover.jpg', 85),
    ('Hotel California', 'Eagles', 'Rock', 1976, 18.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/4/49/Hotelcalifornia.jpg', 84),
    ('21', 'Adele', 'Pop', 2011, 18.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/1/1b/Adele_-_21.png', 83),
    ('Come On Over', 'Shania Twain', 'Pop', 1997, 18.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/c/c3/ShaniaTwain-ComeOnOver.jpg', 82),
    ('Falling into You', 'Celine Dion', 'Pop', 1996, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/4/4e/Fallingintoyou.jpg', 81),
    ('Jagged Little Pill', 'Alanis Morissette', 'Rock', 1995, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b1/Jagged_Little_Pill_album_cover.jpg', 80),
    ('The Bodyguard', 'Whitney Houston', 'Pop', 1992, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/a/a6/Whitney_Houston_-_The_Bodyguard.jpg', 79),
    ('Dirty Dancing', 'Various Artists', 'Pop', 1987, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b8/Dirty_dancing_soundtrack.jpg', 78),
    ('Kind of Blue', 'Miles Davis', 'Jazz', 1959, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/9/9c/MilesDavisKindofBlue.jpg', 77),
    ('Discovery', 'Daft Punk', 'Electronic', 2001, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/2/27/Daft_Punk_-_Discovery.png', 76),
    ('Random Access Memories', 'Daft Punk', 'Electronic', 2013, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/a/a1/Random_Access_Memories.jpg', 75),
    ('Back to Black', 'Amy Winehouse', 'Jazz', 2006, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/6/67/Amy_Winehouse_-_Back_to_Black_%28album%29.png', 74),
    ('OK Computer', 'Radiohead', 'Rock', 1997, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/ba/Radioheadokcomputer.png', 73),
    ('To Pimp a Butterfly', 'Kendrick Lamar', 'Hip-Hop', 2015, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/f/f6/To_Pimp_a_Butterfly.png', 72),
    ('DAMN.', 'Kendrick Lamar', 'Hip-Hop', 2017, 18.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/5/51/Kendrick_Lamar_-_Damn.png', 71),
    ('The Marshall Mathers LP', 'Eminem', 'Hip-Hop', 2000, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/a/ae/The_Marshall_Mathers_LP.jpg', 70),
    ('The Slim Shady LP', 'Eminem', 'Hip-Hop', 1999, 18.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/3/35/Eminem_-_The_Slim_Shady_LP_CD_cover.jpg', 69),
    ('Whatever People Say I Am', 'Arctic Monkeys', 'Rock', 2006, 18.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/c/ca/Arcticmonkeys-wpsiatwin.jpg', 68),
    ('AM', 'Arctic Monkeys', 'Rock', 2013, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/f/f9/Arctic_Monkeys_-_AM.png', 67),
    ('Let It Be', 'The Beatles', 'Rock', 1970, 18.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/4/43/Letitbe.jpg', 66),
    ('Wish You Were Here', 'Pink Floyd', 'Rock', 1975, 18.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/c/c5/WishYouWereHere.jpg', 65),
    ('Off the Wall', 'Michael Jackson', 'Pop', 1979, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/9/91/Michael_Jackson_-_Off_the_Wall.jpg', 64),
    ('Blue', 'Joni Mitchell', 'Jazz', 1971, 19.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/3/3f/Bluealbumcover.jpg', 63),
    ('Born to Run', 'Bruce Springsteen', 'Rock', 1975, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/2/25/Born_to_Run.jpg', 62),
    ('25', 'Adele', 'Pop', 2015, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/c/c2/Adele_-_25.png', 61),
    ('In Utero', 'Nirvana', 'Rock', 1993, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/3/3b/In_Utero_%28album_cover%29.jpg', 60),
    ('Californication', 'Red Hot Chili Peppers', 'Rock', 1999, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/d/df/RedHotChiliPeppersCalifornication.jpg', 59),
    ('Stadium Arcadium', 'Red Hot Chili Peppers', 'Rock', 2006, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/8/8f/Stadium_Arcadium.jpg', 58),
    ('Hybrid Theory', 'Linkin Park', 'Rock', 2000, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/a/a4/Linkin_Park_-_Hybrid_Theory.jpg', 57),
    ('Meteora', 'Linkin Park', 'Rock', 2003, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/4/f9/Linkin_Park-Meteora_album_cover.jpg', 56),
    ('In Rainbows', 'Radiohead', 'Rock', 2007, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/3/3e/In_Rainbows_Official_Cover.jpg', 55),
    ('Homogenic', 'Bjork', 'Electronic', 1997, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/8/8b/Bjork-homogenic.png', 54),
    ('Ray of Light', 'Madonna', 'Pop', 1998, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/5/56/Ray_of_Light_Madonna.png', 53),
    ('Like a Prayer', 'Madonna', 'Pop', 1989, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/6/63/Madonna_-_Like_a_Prayer_album.png', 52),
    ('Graceland', 'Paul Simon', 'Pop', 1986, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/a/a3/Paul_Simon_-_Graceland.jpg', 51);
""")

con.commit()
con.close()
print("✅ 50 albums toegevoegd!")