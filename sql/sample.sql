-- create database glue
--CREATE TABLE IF NOT EXISTS records (
--	id bigserial primary key,
--	mcc INT,
--	merchant VARCHAR(100),
--	currency VARCHAR(10),
--	amount numeric(15,2),
--	transaction_date date,
--	card_type VARCHAR(50),
--	timestamp timestamp default current_timestamp
--);

select * from records r  limit 10;
select max(timestamp) as first_record_ts, min(timestamp) as last_record_ts, max(timestamp) - min(timestamp) as duration from records;
select count(*) from records r;
delete from records;