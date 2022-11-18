create table expense_category(
	id int not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
	name varchar(30) not null,
	color varchar(30) not null,
	user_id int not null, 
	primary key(id),
	foreign key(user_id) references user,
	unique(user_id, name),
	unique(user_id, color)
)

create table expense(
	id int not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
	name varchar(30) not null,
	amount double not null,
	date date not null default CURRENT_DATE,
	category_id int not null,
	primary key(id),
	foreign key(category_id) references expense_category
);