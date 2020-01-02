CREATE TABLE "task" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT
	,"active" INTEGER NOT NULL DEFAULT 0
	,"title" TEXT NOT NULL
	,"description" TEXT
	);

INSERT INTO task ("active", "title", "description") VALUES (1, 'Some Task', 'A first thing to do.');
INSERT INTO task ("active", "title") VALUES (1, 'Another Thing');
INSERT INTO task ("title") VALUES ('Skipped');
INSERT INTO task ("title") VALUES ('Inactive');
INSERT INTO task ("title", "description") VALUES ('Uninteresting', 'Not much to say here.');
INSERT INTO task ("active", "title") VALUES (1, 'Very important');
