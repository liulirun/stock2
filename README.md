# stock2

## Purpose
Home practice for Stock analyze -- a python finance project
created by liulirun@gmail.com at Dec.2020

## How it works
1. download latest stock data from web
2. save data to MySQL docker container
3. analyze the stock data based on MySQL data
4. do regression, find pattern, etc

## Installation Guide
### Python in local windows computer
1. install python 3.14
1. install python .venv under stock2
1. run ```pip install -r .\requirements.txt``` to install python dependency

### Docker
1. install docker desktop in your local ( windows )
1. login
1. run `docker pull liulirun/mysql-stock2` from docker hub,
1. run `docker compose up` from /stockDB/ folder.

### run the code
1. pull this repo
1. create a to cred.py under /credential folder. 
1. run main.py

## Design

- **/credential/**: store credential data,tokens, password, etc.
- **/stockDB/**: maintain mysql container which is runnning in local, including docker-compose, back up scripts.
- **/data/**: for inserting stock data into mysql DB:
  - **fetch_stock_data_from_api.py**: download data from api, generate stock data, then save to local .json.
  - **db_helper.py**: mysql function as read local .json, insert stock_data to DB, fetch stock_data for future use.
  - **stock_data_helper.py**: create moving_average and Bull list for fetch_stock_data_from_api.
  - **json_helper.py**: save, read json file only.
- **/analyze/**: generate daily png and other algos.
  - **draw.py**: draw png for daily stock, including 21 days and 2 years price/vols. Also Gaussian KDE density for 2 years.
  - **algo_daily.py**: daily stock analyze.
  - **algo_regression.py**: regression to see profit.
- **/tests/**: test files. Do not forget the best practice is Continuous Testing.
