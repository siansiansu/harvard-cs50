CREATE TABLE
  users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 10000.00
  );

CREATE TABLE
  sqlite_sequence (name, seq);

CREATE UNIQUE INDEX username ON users (username);

CREATE TABLE
  IF NOT EXISTS "orders" (
    orderid INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    shares TEXT NOT NULL,
    price NUMERIC NOT NULL,
    transacted REAL DEFAULT (datetime ('now', 'localtime')),
    FOREIGN KEY (username) REFERENCES users (username)
  );