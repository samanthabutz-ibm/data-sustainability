USE DATABASE DL_ESG_DEV;
USE SCHEMA CUSTOMER;

-- Create a landing table to store raw JSON data.
-- Snowpipe could load data into this table.
create or replace table _TMP_CUSTOMER (var variant);
create or replace table _TMP_PORTFOLIO (var variant);


-- Create a stream to capture inserts to the landing table.
-- A task will consume a set of columns from this stream.
create or replace stream customer_stream on table _TMP_CUSTOMER;
create or replace stream portfolio_stream on table _TMP_PORTFOLIO;

copy into _TMP_customer
    from @DL_ESG_DEV.external_stages.aws_stage/coc/customer/ 
    file_format= DL_ESG_DEV.CUSTOMER.raw_json_format
    on_error = continue 
    FORCE = true;
    
select * from _TMP_CUSTOMER;

select * from customer_stream;



-- Create a task that inserts new name records from the rawstream1 stream into the names table
-- every minute when the stream contains records.
-- Replace the 'mywh' warehouse with a warehouse that your role has USAGE privilege on.
create or replace task tmp_to_customer
warehouse = WH_ESG_SUSTAINABILITY
schedule = '60 minutes'
when
system$stream_has_data('customer_stream')
as
merge into customer c
  using (select var:C_ID C_ID, var:FIRST_NAME FIRST_NAME, var:LAST_NAME LAST_NAME, var:EMAIL EMAIL, var:GENDER GENDER, var:AGE AGE, var:PORTFOLIO_ID PORTFOLIO_ID from customer_stream) r1 on c.C_ID = r1.C_ID
  when matched then update set c.FIRST_NAME = r1.FIRST_NAME, c.LAST_NAME = r1.LAST_NAME, c.EMAIL = r1.EMAIL, c.GENDER = r1.GENDER, c.AGE = r1.AGE, c.PORTFOLIO_ID = r1.PORTFOLIO_ID
  when not matched then insert (C_ID, FIRST_NAME, LAST_NAME, EMAIL, GENDER, AGE, PORTFOLIO_ID) values (r1.C_ID, r1.FIRST_NAME, r1.LAST_NAME, r1.EMAIL, r1.GENDER, r1.AGE, r1.PORTFOLIO_ID)
;



-- Resume both tasks.
alter task tmp_to_customer resume;

-- Suspend both tasks.
alter task tmp_to_customer suspend;

-- Wait for the tasks to run.
call system$wait(70);


select * from customer;
TRUNCATE TABLE customer;




