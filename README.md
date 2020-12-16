# stock2

This is home practice for Stock analyze -- a python finance project

1. download stock data from web
2. store data to MySQL docker container
3. analyze the stock data based on MySQL data
4. do regression, find pattern, etc

Design:
/credential: store credential data, like tokens, password
/mysql: for maintaining mysql container runnning in local, includes docker-compose, back up script
/data: for inserting stock data into mysql DB

/data/api_hub: 
download data from api. 
import stock_data_helper to generate stock data
import json_helper to save json


/data/db_helper:
DB api (create, update, read, etc)
generating stock_list- import json_helper to read json, then use insert_stock_data_to_db to create the stock_list


/data/stock_data_helper:
create moving_average list
create BULL list for api_hub to use, save to json for later


/data/json_helper:
save, read json file only




