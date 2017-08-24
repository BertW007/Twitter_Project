CREATE TABLE Users (
	user_id int AUTO_INCREMENT,
	name varchar(255),
	hashed_password varchar(255),
	email varchar(255) UNIQUE,
	PRIMARY KEY(user_id))