CREATE USER morse;
CREATE DATABASE morse;
GRANT ALL PRIVILEGES ON morse.* TO 'morse'@'localhost' IDENTIFIED BY 'morse';
GRANT ALL PRIVILEGES ON morse.* TO 'morse'@'%' IDENTIFIED BY 'morse';
USE morse;
CREATE TABLE morse (
    `Character` VARCHAR(1) CHARACTER SET utf8,
    `Code` VARCHAR(6) CHARACTER SET utf8,
    PRIMARY KEY (`Character`)
);
LOAD DATA LOCAL INFILE "morse.csv" INTO TABLE morse.morse FIELDS TERMINATED BY '$' LINES TERMINATED BY '\n';
