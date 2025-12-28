-- table_text
UPDATE table_text
SET
  title    = REGEXP_REPLACE(REGEXP_REPLACE(title,    '-\\s+', ''), ';([^\\s])', '; \\1'),
  option_1 = REGEXP_REPLACE(REGEXP_REPLACE(option_1, '-\\s+', ''), ';([^\\s])', '; \\1'),
  option_2 = REGEXP_REPLACE(REGEXP_REPLACE(option_2, '-\\s+', ''), ';([^\\s])', '; \\1'),
  option_3 = REGEXP_REPLACE(REGEXP_REPLACE(option_3, '-\\s+', ''), ';([^\\s])', '; \\1'),
  option_4 = REGEXP_REPLACE(REGEXP_REPLACE(option_4, '-\\s+', ''), ';([^\\s])', '; \\1'),
  option_5 = REGEXP_REPLACE(REGEXP_REPLACE(option_5, '-\\s+', ''), ';([^\\s])', '; \\1'),
  option_6 = REGEXP_REPLACE(REGEXP_REPLACE(option_6, '-\\s+', ''), ';([^\\s])', '; \\1');

-- combat_texts
UPDATE combat_texts
SET text = REGEXP_REPLACE(REGEXP_REPLACE(text, '-\\s+', ''), ';([^\\s])', '; \\1');

-- info_lines
UPDATE info_lines
SET text = REGEXP_REPLACE(REGEXP_REPLACE(text, '-\\s+', ''), ';([^\\s])', '; \\1');

USE webtorkel;

UPDATE table_text
SET
  label   = TRIM(REGEXP_REPLACE(label,   '[[:space:]]+', ' ')),
  title   = TRIM(REGEXP_REPLACE(title,   '[[:space:]]+', ' ')),
  option_1= TRIM(REGEXP_REPLACE(option_1,'[[:space:]]+', ' ')),
  option_2= TRIM(REGEXP_REPLACE(option_2,'[[:space:]]+', ' ')),
  option_3= TRIM(REGEXP_REPLACE(option_3,'[[:space:]]+', ' ')),
  option_4= TRIM(REGEXP_REPLACE(option_4,'[[:space:]]+', ' ')),
  option_5= TRIM(REGEXP_REPLACE(option_5,'[[:space:]]+', ' ')),
  option_6= TRIM(REGEXP_REPLACE(option_6,'[[:space:]]+', ' '));