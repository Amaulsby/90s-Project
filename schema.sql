DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);


INSERT INTO users (username, password) VALUES
  ('admin',      'admin123'),
  ('acidburn',   'hacktheplanet'),
  ('zerocool',   'crashoverride'),
  ('thementor',  '414manifesto');
