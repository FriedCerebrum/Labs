CREATE TABLE subject
(
	id serial PRIMARY KEY,
	name varchar(128) NOT NULL
);

CREATE TABLE subject_type
(
	id serial PRIMARY KEY,
	name varchar(128) NOT NULL
);

CREATE TABLE class
(
	id serial PRIMARY KEY,
	subject int NOT NULL REFERENCES subject(id),
	subject_type int NOT NULL REFERENCES subject_type(id)
);

CREATE TABLE time
(
	id serial PRIMARY KEY,
	start_time varchar(64) NOT NULL
);


CREATE TABLE teacher
(
	id serial PRIMARY KEY,
	full_name varchar(256) NOT NULL
);

CREATE TABLE teacher_subject
(
	id serial PRIMARY KEY,
	teacher int NOT NULL REFERENCES teacher(id),
	class int NOT NULL REFERENCES class(id)
);

CREATE TABLE timetable
(
	id serial PRIMARY KEY,
	week int NOT NULL,
	day int NOT NULL,
	class int NOT NULL REFERENCES class(id),
	class_time int NOT NULL REFERENCES time(id),
	room_number varchar(64) NOT NULL
);
