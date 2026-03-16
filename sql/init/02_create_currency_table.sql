create table if not exists currency (
    id serial primary key,
    name varchar(100) not null,
    symbol varchar(20)
)