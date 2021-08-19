from mysql.models import db, Link, Advertisement, Company, Tag

#  run this file only one time in order to create the tables on sql

if __name__ == "__main__":
    db.create_tables([Link, Advertisement, Tag, Company])
