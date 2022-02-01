import sqlite3

connexion = sqlite3.connect('nominations.db')
connexion.execute('pragma table_info(nominations)').fetchall()

year_host =[(2010, 'Steve Martin'),
(2009, 'Hugh Jackman'),
(2008, 'Jon Stewart'),
(2007, 'Ellen DeGeneres'),
(2006, 'Jon Stewart'),
(2005, 'Chris Rock'),
(2004, 'Billy Crystal'),
(2003, 'Steve Martin'),
(2002, 'Whoopi Goldberg'),
(2001, 'Steve Martin'),
(2000, 'Billy Crystal')]

connexion.execute('CREATE TABLE ceremonies(id integer PRIMARY KEY, Year integer, Host text);').fetchall()
connexion.execute('SELECT name FROM sqlite_master WHERE type="table"').fetchall()

query = 'INSERT INTO ceremonies(Year, Host) VALUES (?,?);'
connexion.executemany(query, year_host).fetchall()

connexion.commit()

connexion.execute('pragma foreign_keys = on;').fetchall()
connexion.execute('CREATE TABLE nominations_2(id integer PRIMARY KEY, Ceremony_id integer REFERENCES ceremonies(id), Category text, Nominee text, Movie text, Character text, Won integer);').fetchall()
connexion.execute('pragma table_info(nominations_2);').fetchall()

join_nominations_query = 'SELECT nominations.Category, nominations.Nominee, nominations.Movie, nominations.Character, nominations.Won, ceremonies.id FROM nominations INNER JOIN ceremonies ON nominations.year == ceremonies.year;'
join_nominations = connexion.execute(join_nominations_query).fetchall()

query2= 'INSERT INTO nominations_2(Category, Nominee, Movie, Character, Won, Ceremony_id) VALUES(?,?,?,?,?,?)'

connexion.executemany(query2, join_nominations).fetchall()

connexion.commit()

connexion.execute('DROP TABLE nominations').fetchall()
connexion.execute('ALTER TABLE nominations_2 RENAME TO nominations').fetchall()

# Création des tables
connexion.execute('CREATE TABLE movies(id integer PRIMARY KEY, Movie text);').fetchall()
connexion.execute('CREATE TABLE actors(id integer PRIMARY KEY, Actor text);').fetchall()

#Récupération des informations
movies = connexion.execute('SELECT DISTINCT Movie FROM nominations;').fetchall()
actors = connexion.execute('SELECT DISTINCT Nominee FROM nominations;').fetchall()

#Injection des informations dans les tables
connexion.executemany('INSERT INTO movies(Movie) VALUES (?);', movies).fetchall()
connexion.executemany('INSERT INTO actors(Actor) VALUES (?);', actors).fetchall()

#Création de la Join table
connexion.execute('CREATE TABLE movies_actors(id integer PRIMARY KEY, movies_id integer REFERENCES movies(id), actors_id integer REFERENCES actors(id));').fetchall()

connexion.commit()

movies_actors = connexion.execute('SELECT movies.id, actors.id FROM movies INNER JOIN nominations ON movies.Movie == nominations.Movie INNER JOIN actors ON nominations.Nominee == actors.Actor;').fetchall()
connexion.executemany('INSERT INTO movies_actors VALUES (null,?,?)', movies_actors).fetchall()

connexion.commit()
