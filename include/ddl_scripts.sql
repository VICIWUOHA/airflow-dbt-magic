--Syntax: PostgreSql
-- Execute against Data Warehouse

DROP TABLE IF EXISTS airflow_dbt_magic.products;
CREATE TABLE IF NOT EXISTS airflow_dbt_magic.products(
    id numeric, 
    title varchar, 
    price numeric, 
    description varchar,
    category varchar, 
    image varchar, 
    rating_rate decimal, 
    rating_count numeric,
    _dbt_meetup_user varchar,
    uuid varchar primary key

);

DROP TABLE IF EXISTS airflow_dbt_magic.users;
CREATE TABLE IF NOT EXISTS airflow_dbt_magic.users(
    id numeric, 
    email varchar, 
    username varchar,
    phone varchar,
    address_geolocation_lat numeric,
    address_geolocation_long numeric, 
    address_city varchar, 
    address_street varchar, 
    address_number numeric, 
    address_zipcode varchar, 
    firstname varchar, 
    lastname varchar,
    _dbt_meetup_user varchar,
    uuid varchar primary key

);

DROP TABLE IF EXISTS airflow_dbt_magic.carts;
CREATE TABLE IF NOT EXISTS airflow_dbt_magic.carts(
    cart_id numeric,
	id varchar,
    date date,
    user_id numeric,
    product_id numeric,
    quantity numeric,
    _dbt_meetup_user varchar,
    uuid varchar primary key

);

