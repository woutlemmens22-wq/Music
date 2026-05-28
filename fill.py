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
    ('Speak to Me', 'Coldplay', 'Rock', 2002, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/f/f6/Coldplay_-_A_Rush_of_Blood_to_the_Head.png', 50),
    ('X&Y', 'Coldplay', 'Rock', 2005, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/5/5f/Coldplay_-_X%26Y.png', 49),
    ('Is This It', 'The Strokes', 'Rock', 2001, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/1/1f/Is_This_It_album_cover.jpg', 48),
    ('Elephant', 'The White Stripes', 'Rock', 2003, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/4/4d/White_Stripes_-_Elephant.png', 47),
    ('Turn On the Bright Lights', 'Interpol', 'Rock', 2002, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/a/a4/Turnonthebrightlights.jpg', 46),
    ('Franz Ferdinand', 'Franz Ferdinand', 'Rock', 2004, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/6/63/FranzFerdinand-FranzFerdinand.jpg', 45),
    ('Hot Fuss', 'The Killers', 'Rock', 2004, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b8/Hot_Fuss.png', 44),
    ('Sam Town', 'The Killers', 'Rock', 2006, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/7/73/TheKillers-SamsClub.jpg', 43),
    ('White Blood Cells', 'The White Stripes', 'Rock', 2001, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/f/f9/White_Blood_Cells.jpg', 42),
    ('Funeral', 'Arcade Fire', 'Rock', 2004, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b8/Arcade_Fire_-_Funeral.png', 41),
    ('Neon Bible', 'Arcade Fire', 'Rock', 2007, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/3/thirty/Arcade_Fire_-_Neon_Bible.png', 40),
    ('Sound of Silver', 'LCD Soundsystem', 'Electronic', 2007, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/4/forty/LCD_Soundsystem_-_Sound_of_Silver.jpg', 39),
    ('American Dream', 'LCD Soundsystem', 'Electronic', 2017, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b6/LCD_Soundsystem_-_American_Dream.jpg', 38),
    ('Currents', 'Tame Impala', 'Electronic', 2015, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/9/9b/Tame_Impala_-_Currents.png', 37),
    ('Lonerism', 'Tame Impala', 'Rock', 2012, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/3/3c/Tame_Impala_-_Lonerism.png', 36),
    ('Demon Days', 'Gorillaz', 'Electronic', 2005, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/3/thirty/Gorillaz_-_Demon_Days.png', 35),
    ('Gorillaz', 'Gorillaz', 'Electronic', 2001, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/e/e1/GorillazAlbumcover.jpg', 34),
    ('Plastic Beach', 'Gorillaz', 'Electronic', 2010, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/2/2f/Gorillaz_-_Plastic_Beach.png', 33),
    ('Since I Left You', 'The Avalanches', 'Electronic', 2000, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/4/4b/The_Avalanches_-_Since_I_Left_You.jpg', 32),
    ('Dummy', 'Portishead', 'Electronic', 1994, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/6/6c/PortisheadDummyalbum.jpg', 31),
    ('Mezzanine', 'Massive Attack', 'Electronic', 1998, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/d/d5/MassiveAttackMezzanine.jpg', 30),
    ('Blue Lines', 'Massive Attack', 'Electronic', 1991, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/c/c9/Massive_Attack_-_Blue_Lines.jpg', 29),
    ('Protection', 'Massive Attack', 'Electronic', 1994, 15.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/8/8b/Massive_Attack_-_Protection.jpg', 28),
    ('Trip Hop Classics', 'Tricky', 'Electronic', 1995, 15.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b4/Tricky-maxinquaye.jpg', 27),
    ('Section.80', 'Kendrick Lamar', 'Hip-Hop', 2011, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/6/6a/Section.80.jpg', 26),
    ('Mr. Morale', 'Kendrick Lamar', 'Hip-Hop', 2022, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b9/Kendrick_Lamar_-_Mr._Morale_%26_The_Big_Steppers.png', 25),
    ('Madvillainy', 'Madvillain', 'Hip-Hop', 2004, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/0/0f/Madvillainy.jpg', 24),
    ('Donuts', 'J Dilla', 'Hip-Hop', 2006, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/0/0a/J_Dilla_-_Donuts_%28album_cover%29.jpg', 23),
    ('Moment of Truth', 'Gang Starr', 'Hip-Hop', 1998, 15.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b3/Gang_Starr_-_Moment_of_Truth.jpg', 22),
    ('Southernplayalisticadillacmuzik', 'Outkast', 'Hip-Hop', 1994, 15.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/2/2d/Outkast-southernplayalisticadillacmuzik.jpg', 21),
    ('ATLiens', 'Outkast', 'Hip-Hop', 1996, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b4/OutKast_ATLiens.jpg', 20),
    ('Enter the Wu-Tang', 'Wu-Tang Clan', 'Hip-Hop', 1993, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/be/Enter_the_Wu-Tang_36_Chambers.jpg', 19),
    ('Reasonable Doubt', 'Jay-Z', 'Hip-Hop', 1996, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/e/e3/Jay-Z_-_Reasonable_Doubt.jpg', 18),
    ('All Eyez on Me', 'Tupac', 'Hip-Hop', 1996, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/a/a9/Alleyezonme.jpg', 17),
    ('Me Against the World', 'Tupac', 'Hip-Hop', 1995, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/e/e3/MeAgainsttheWorld.jpg', 16),
    ('The Miseducation of Lauryn Hill', 'Lauryn Hill', 'Hip-Hop', 1998, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/a/a8/Lauryn_Hill_-_The_Miseducation_of_Lauryn_Hill.jpg', 15),
    ('Midnight Marauders', 'A Tribe Called Quest', 'Hip-Hop', 1993, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/d/d4/ATCQMidnightMarauders.jpg', 14),
    ('The Low End Theory', 'A Tribe Called Quest', 'Hip-Hop', 1991, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/0/0e/ATCQ_The_Low_End_Theory.jpg', 13),
    ('Paid in Full', 'Eric B. and Rakim', 'Hip-Hop', 1987, 15.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/4/4f/Eric_B._and_Rakim_-_Paid_in_Full.jpg', 12),
    ('It Takes a Nation', 'Public Enemy', 'Hip-Hop', 1988, 15.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/9/9f/ItTakesaNationofMillionstoHoldUsBack.jpg', 11),
    ('Paul Boutique', 'Beastie Boys', 'Hip-Hop', 1989, 15.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/6/6e/PaulsBoutique.jpg', 10),
    ('Licensed to Ill', 'Beastie Boys', 'Hip-Hop', 1986, 15.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/b/b8/Licensed_to_Ill.jpg', 9),
    ('Chronic', 'Dr. Dre', 'Hip-Hop', 1992, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/1/19/Dr.DreTheChronic.jpg', 8),
    ('2001', 'Dr. Dre', 'Hip-Hop', 1999, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/4/4f/Dr._Dre_-_2001.jpg', 7),
    ('Straight Outta Compton', 'N.W.A', 'Hip-Hop', 1988, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/4/forty/Straight_outta_compton.jpg', 6),
    ('Ready to Die', 'The Notorious B.I.G.', 'Hip-Hop', 1994, 17.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/5/5d/ReadyToDie.jpg', 5),
    ('Life After Death', 'The Notorious B.I.G.', 'Hip-Hop', 1997, 16.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/3/3c/Life_After_Death.jpg', 4),
    ('Only Built 4 Cuban Linx', 'Raekwon', 'Hip-Hop', 1995, 15.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/c/c3/Raekwon-onlybuilt4cubanlinx.jpg', 3),
    ('Raising Hell', 'Run-DMC', 'Hip-Hop', 1986, 15.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/a/a4/Run_DMC_-_Raising_Hell.jpg', 2),
    ('Kings of Rock', 'Run-DMC', 'Hip-Hop', 1985, 14.99, 'cd', 'https://upload.wikimedia.org/wikipedia/en/f/f3/Run-DMC_-_King_of_Rock.jpg', 1);
""")

con.commit()
con.close()
print("✅ 50 nieuwe albums toegevoegd!")