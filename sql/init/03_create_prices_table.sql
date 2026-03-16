create table if not exists prices (
    id serial primary key,
    coin_id int not null,
    currency_id int not null,
    price numeric(20, 10) not null,
    last_updated_at timestamp not null,
    created_at timestamptz default current_timestamp,
    foreign key (coin_id) references crypto_currency(id),
    foreign key (currency_id) references currency(id),
    unique(coin_id, currency_id, last_updated_at),
    check (price >= 0)
    
)