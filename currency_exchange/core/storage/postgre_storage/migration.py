MIGRATION_SCRIPT = """
create table currency
(
  code varchar(100) primary key,
  name varchar(100) null
);

create table provider
(
  code varchar(100) primary key,
  name varchar(100) not null
);

create table currency_exchange_rate
(
  id serial primary key ,
  from_currency_id varchar(100) not null references currency(code),
  to_currency_id varchar(100) not null references currency(code),
  on_date timestamp not null ,
  provider_id varchar(100) not null references provider(code),
  rate numeric(24, 12) not null check ( rate > 0.0 ),

  constraint currency_exchange_rate_unique unique (from_currency_id, to_currency_id, provider_id, on_date)
);
"""