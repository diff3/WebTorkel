CREATE DATABASE IF NOT EXISTS webtorkel CHARACTER SET utf8mb4 COLLATE utf8mb4_swedish_ci;
USE webtorkel;

CREATE TABLE IF NOT EXISTS table_text (
  table_id INT NOT NULL,
  label TEXT,
  title TEXT,
  option_1 TEXT,
  option_2 TEXT,
  option_3 TEXT,
  option_4 TEXT,
  option_5 TEXT,
  option_6 TEXT,
  PRIMARY KEY (table_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

CREATE TABLE IF NOT EXISTS table_option_properties (
  table_id INT NOT NULL,
  option_index INT NOT NULL,
  c0 INT NOT NULL,
  c1 INT NOT NULL,
  c2 INT NOT NULL,
  c3 INT NOT NULL,
  c4 INT NOT NULL,
  c5 INT NOT NULL,
  c6 INT NOT NULL,
  c7 INT NOT NULL,
  c8 INT NOT NULL,
  c9 INT NOT NULL,
  c10 INT NOT NULL,
  c11 INT NOT NULL,
  c12 INT NOT NULL,
  c13 INT NOT NULL,
  c14 INT NOT NULL,
  c15 INT NOT NULL,
  c16 INT NOT NULL,
  c17 INT NOT NULL,
  c18 INT NOT NULL,
  c19 INT NOT NULL,
  c20 INT NOT NULL,
  c21 INT NOT NULL,
  c22 INT NOT NULL,
  c23 INT NOT NULL,
  c24 INT NOT NULL,
  c25 INT NOT NULL,
  c26 INT NOT NULL,
  c27 INT NOT NULL,
  c28 INT NOT NULL,
  c29 INT NOT NULL,
  c30 INT NOT NULL,
  c31 INT NOT NULL,
  c32 INT NOT NULL,
  c33 INT NOT NULL,
  c34 INT NOT NULL,
  c35 INT NOT NULL,
  c36 INT NOT NULL,
  c37 INT NOT NULL,
  PRIMARY KEY (table_id, option_index)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

CREATE TABLE IF NOT EXISTS opponents (
  opponent_id INT NOT NULL,
  correction INT NOT NULL,
  xp INT NOT NULL,
  PRIMARY KEY (opponent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

CREATE TABLE IF NOT EXISTS combat_texts (
  combat_id INT NOT NULL,
  text TEXT,
  PRIMARY KEY (combat_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;

CREATE TABLE IF NOT EXISTS info_lines (
  line_index INT NOT NULL,
  text TEXT,
  PRIMARY KEY (line_index)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_swedish_ci;
