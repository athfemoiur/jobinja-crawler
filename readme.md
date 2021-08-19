# Jobinja website crawler (python)

Hello everybody, this is a crawler (scrapper)  for jobinja website with python

***

Jobinja is a website where you can see thousands of recruitment advertisements. In this crawler I focus on the advertisements related to programming and coding :)

#### NOTE : turn on your vpn before running any part of the project related to network if you are living in Iran :)

## Tools used 
I have used python for writing this crawler, in addition I've used libraries and packages like (requests, selenium, pymongo, peewee, beautifulsoup, ...)

## Features

This is somehow a complete crawler. As I said it's only used for the advertisements related to programming and coding of this website.
 
* You are able to select which city to be crawled
* You can save the crawled data

There are two options for saving the data:
* Mysql
* Mongodb




## Installation

First of all clone the project

```bash
https://github.com/athfemoiur/jobinja-crawler.git
```
For this project you need to have mysql-server or mongodb or both of them installed.

***
##### Only for mysql :
Use terminal to create a new user if you don't have already then create a new database ( remember this information , we need them later)
***


We need a virtual environment you can create like this : 

```bash
virtualenv venv
```
Then activate it
```bash
source venv/bin/activate
```
Now install all of the packages in requirements.txt file in project directory 
```bash
pip install -r requirements.txt
```
***
##### Only for mysql :
Go to mysql/mysql_config.py file and change the value of the variables to config your database
```python
USER_NAME = "amir"

PASSWORD = "1234"

DATABASE_NAME = 'jobinja'
```

You need to run mysql/create_table.py file just one time to create the tables in your database just one time
***
## Usage
crawling and saving advertisements  links : First you can change the city from config.py file(the name of city must be in Persian language). Then you can choose your database (mongodb or mysql). Now you can run the crawler using the following command
```bash
python main.py link
```
crawling and saving advertisements data : Now you can collect the data of advertisements which you have saved the links earlier

For mysql use this command : 
```bash
python main.py datamysql
```

For mongodb use this command : 
```bash
python main.py datamongo
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
