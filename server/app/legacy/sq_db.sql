CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS logs (
id integer PRIMARY KEY AUTOINCREMENT,
login text NOT NULL,
password text NOT NULL
);