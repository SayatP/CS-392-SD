create table products (
    id serial primary key,
    image_src varchar (256),
    price decimal(12, 2),
    title varchar(256),
    quantity int default 100,
    date_added date default current_timestamp
);
