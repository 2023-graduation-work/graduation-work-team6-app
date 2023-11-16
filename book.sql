CREATE TABLE book (
  id SERIAL PRIMARY KEY,
  title VARCHAR(64),
  author VARCHAR(64),
  company VARCHAR(64),
  ISBN VARCHAR(13)
);

CREATE TABLE list (
  title VARCHAR(64),
  user_name VARCHAR(64),
  mail VARCHAR(64),
  ISBN VARCHAR(13),
  lend_date DATE
);