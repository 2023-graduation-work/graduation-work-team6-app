CREATE TABLE book (
  id SERIAL PRIMARY KEY,
  title VARCHAR(64),
  author VARCHAR(64),
  company VARCHAR(64),
  ISBN VARCHAR(13)
);