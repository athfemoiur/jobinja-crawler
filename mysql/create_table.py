from mysql.models import db, Link, Advertisement, Company, Tag

#  run this file only one time in order to create the tables on sql

db.create_tables([Link, Advertisement, Tag, Company])
