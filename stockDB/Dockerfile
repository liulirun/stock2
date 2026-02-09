FROM mysql:latest

# Set environment variables for the database
ENV MYSQL_ROOT_PASSWORD=mysql_pass
ENV MYSQL_DATABASE=stock

# Copy the SQL dump file into the container's initialization directory
# Docker automatically runs .sql files placed in this directory on first start
COPY bk_stock.sql /docker-entrypoint-initdb.d/

# docker build -t test-mysql-image .
# docker run -d --name my-custom-db -p 3306:3306 test-mysql-image

# show databases; use stock; show tables like 'US_BABA'; select * from US_BABA limit 1;
