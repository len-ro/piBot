create table sensor_data (capture_time timestamp, id varchar(256), name varchar(256), value numeric);
create unique index sensor_data_index on sensor_data (capture_time, id);