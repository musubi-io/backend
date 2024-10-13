-- DROP TABLE IF EXISTS userEmail;
-- DROP TABLE IF EXISTS phishingEmail;
-- DROP TABLE IF EXISTS scoring;

CREATE TABLE userEmail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE phishingEmail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname TEXT NOT NULL,
    email_subject TEXT NOT NULL,
    email_body TEXT NOT NULL
);
CREATE TABLE scoring(
    user_id INT REFERENCES userEmail(id),
    email_id INT REFERENCES phishingEmail(id),
    reply TEXT,
    linkClicked BOOLEAN NOT NULL,
    timespent INT NOT NULL,
    opened BOOLEAN NOT NULL,
    date_sent DATE NOT NULL,
    feedback TEXT NOT NULL
);
