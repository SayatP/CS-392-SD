create table products (
    id serial primary key,
    image_src varchar (256),
    price decimal(12, 2),
    title varchar(256),
    quantity int default 100,
    date_added date default current_timestamp
);


create table users (
    id serial primary key,
    first_name varchar(256),
    last_name varchar(256),
    address varchar(256),
    email varchar(256),
    phone_number varchar(64),
    register_date date default current_timestamp
);
