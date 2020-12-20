<h1>stock2</h1>

<h2>Purpose</h2>

Home practice for Stock analyze -- a python finance project
created by liulirun@gmail.com at Dec.2020

<h2>Scenarios</h2>

1. download latest stock data from web
2. save data to MySQL docker container
3. analyze the stock data based on MySQL data
4. do regression, find pattern, etc

<h2>Install</h2>

1. install docker in your local
2. docker pull [mysql-stock2](https://hub.docker.com/repository/docker/liulirun/mysql-stock2) from docker hub, or run /mysql/docker-compose.yaml. It is private for now, contact liulirun@gmail.com for access.
3. install python 3.8 and pip. 
4. pip install dependencies: MySQLdb, docker, requests, json, pandas, numpy, matplotlib, scipy, mock.
5. pull this repo
6. rename /credential/example.py to cred.py
7. run main.py


<h2>Design</h2>

- **/credential/**: store credential data,tokens, password, etc.
- **/mysql/**: maintain mysql container which is runnning in local, including docker-compose, back up scripts.
- **/data/**: for inserting stock data into mysql DB:
    - **api_hub.py**: download data from api, generate stock data, then save to local .json.
    - **db_helper.py**: mysql function as read local .json, insert stock_data to DB, fetch stock_data for future use.
    - **stock_data_helper.py**: create moving_average and Bull list for api_hub.
    - **json_helper.py**: save, read json file only.
- **/analyze/**: generate daily png and other algos. 
    - **draw.py**: draw png for daily stock, including 21 days and 2 years price/vols. Also Gaussian KDE density for 2 years.
    - **algo_current.py**: daily stock analyze.
- **/tests/**: test files. Do not forget the best practice is Continuous Testing.


<h2>Misc</h2>








