BEGIN TRANSACTION;
CREATE TABLE "users" (
	`user_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`username`	TEXT,
	`password`	TEXT,
	`list_allowed_id`	INTEGER,
	`type`	TEXT
);
INSERT INTO `users` (user_id,username,password,list_allowed_id,type) VALUES (1,'user','pass',1,'user'),
 (2,'user2','pass',2,'user'),
 (3,'manager','pass',NULL,'manager');
CREATE TABLE "todo_lists" (
	`todo_list_id`	INTEGER,
	`todo_list_name`	TEXT,
	PRIMARY KEY(todo_list_id)
);
INSERT INTO `todo_lists` (todo_list_id,todo_list_name) VALUES (1,'Shopping list'),
 (2,'Read cool books'),
 (3,'Collect money'),
 (4,'This week'),
 (5,'Baby'),
 (6,'Auto');
CREATE TABLE "todo_items" (
	`item_id`	INTEGER,
	`item_content`	TEXT,
	`todo_list_id`	INTEGER,
	`done`	TEXT,
	`priority`	INTEGER,
	`due_date`	TEXT,
	`creation_date`	TEXT,
	PRIMARY KEY(item_id)
);
INSERT INTO `todo_items` (item_id,item_content,todo_list_id,done,priority,due_date,creation_date) VALUES (1,'Beers',1,'False',10,'2017-03-22','2017-03-04'),
 (2,'Bread',1,'False',2,'2017-03-14','2017-03-04'),
 (3,'Milk',1,'False',4,'2017-03-14','2017-03-04'),
 (4,'Coffee',1,'False',6,'2017-03-25','2017-03-04'),
 (5,'Harry Potter1',2,'False',2,'2017-03-08','2017-03-04'),
 (6,'Harry Barry',2,'False',6,'2017-03-14','2017-03-04'),
 (7,'Hemingway best of',2,'False',9,'2017-03-08','2017-03-04'),
 (8,'from Robert',3,'False',2,'2017-03-07','2017-03-04'),
 (9,'from John',3,'False',6,'2017-03-11','2017-03-04'),
 (10,'from Andrew',3,'False',9,'2017-03-15','2017-03-04'),
 (11,'from Tom',3,'False',10,'2017-03-31','2017-03-04'),
 (12,'make party ',4,'False',10,'2017-03-10','2017-03-04'),
 (13,'sell car',4,'False',1,'2017-03-05','2017-03-04'),
 (14,'help my aunt',4,'False',9,'2017-03-03','2017-03-04'),
 (15,'help Jane',4,'False',0,'2017-03-02','2017-03-04'),
 (16,'buy food',5,'False',3,'','2017-03-04'),
 (17,'buy toys',5,'False',3,'2017-03-10','2017-03-04'),
 (18,'play with child',5,'False',8,'','2017-03-04'),
 (19,'clean',6,'False',3,'','2017-03-04'),
 (20,'load gas',6,'False',8,'2017-03-22','2017-03-04'),
 (21,'drive fast',6,'False',10,'2017-03-14','2017-03-04'),
 (22,'sell it',6,'False',3,'','2017-03-04');
CREATE TABLE `lists_allowed` (
	`id`	INTEGER,
	`user_id`	INTEGER,
	`list_id`	INTEGER,
	PRIMARY KEY(id)
);
INSERT INTO `lists_allowed` (id,user_id,list_id) VALUES (1,2,1),
 (2,2,2),
 (3,2,3),
 (4,1,1),
 (5,1,3),
 (6,1,4),
 (7,1,5),
 (8,1,6);
COMMIT;
