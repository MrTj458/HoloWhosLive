-- upgrade --
CREATE TABLE IF NOT EXISTS "twitchchannel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "last_name" VARCHAR(255) NOT NULL,
    "first_name" VARCHAR(255) NOT NULL,
    "channel_id" VARCHAR(255) NOT NULL,
    "group_id" INT NOT NULL REFERENCES "group" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "twitchchannel";
