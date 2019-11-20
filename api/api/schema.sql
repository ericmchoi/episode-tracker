DROP TABLE IF EXISTS show;

CREATE TABLE show (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    totalEpisodes INTEGER NOT NULL,
    lastEpisode INTEGER NOT NULL,
    link TEXT
);

INSERT INTO show (title, totalEpisodes, lastEpisode, link) VALUES ('hello', 23, 11, 'https://www.google.com');