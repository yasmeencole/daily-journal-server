CREATE TABLE `Entry` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept`    TEXT NOT NULL,
    `entry`    TEXT NOT NULL,
    `date`    DATETIME NOT NULL,
    `mood_id`    INTEGER NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)

);

CREATE TABLE `Mood` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`label`	TEXT NOT NULL
);

INSERT INTO `Entry` VALUES (null, "Because I am Happy", "Today was a good day", "04/19/2020", 1);
INSERT INTO `Entry` VALUES (null, "Today was a really long day.", "04/21/2020", 4);
INSERT INTO `Entry` VALUES (null, "Python", "Python is okay so far.", "04/22/2020", 1);


INSERT INTO `Mood` VALUES (null, "Happy");
INSERT INTO `Mood` VALUES (null, "Sad");
INSERT INTO `Mood` VALUES (null, "Angry");
INSERT INTO `Mood` VALUES (null, "Okay");
