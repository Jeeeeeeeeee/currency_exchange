MIGRATION_SCRIPT = """
create table currency
(
  code text primary key not null,
  name text null
);

create table provider
(
  code text primary key not null,
  name text not null
);

create table currency_exchange_rate
(
  id integer primary key ,
  from_currency_id text not null ,
  to_currency_id text not null ,
  on_date numeric not null ,
  provider_id text not null,
  rate real not null check ( rate > 0.0 ),

  foreign key (from_currency_id) references currency(code),
  foreign key (to_currency_id) references currency(code),
  foreign key (provider_id) references provider(code),
  unique (from_currency_id, to_currency_id, provider_id, on_date)
);
"""