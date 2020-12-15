CREATE TABLE IF NOT EXISTS allowed_channels (
    `id` INT NOT NULL AUTO_INCREMENT, 
    `channel_id` TINYTEXT NOT NULL, 
    `allowed` BOOL NOT NULL,
    PRIMARY KEY(id)
);
CREATE TABLE IF NOT EXISTS messages (
    `id` INT NOT NULL AUTO_INCREMENT, 
    `sentences` TEXT, 
    `replies` LONGTEXT,
    PRIMARY KEY(id)
);