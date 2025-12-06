DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- Dummy 90s-hacker-style users with plain-text passwords (demo only)
INSERT INTO users (username, password) VALUES
  ('admin',      'admin123'),
  ('acidburn',   'hacktheplanet'),
  ('zerocool',   'crashoverride'),
  ('thementor',  '414manifesto');
