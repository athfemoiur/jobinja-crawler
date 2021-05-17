from peewee import Model, TextField, CharField, ForeignKeyField, BooleanField

from mysql.connector import db


class BaseModel(Model):
    class Meta:
        database = db


class Link(BaseModel):
    url = TextField()
    flag = BooleanField()


class Company(BaseModel):
    name = CharField()
    description = TextField()


class Advertisement(BaseModel):
    link = ForeignKeyField(Link, backref="advertisement")
    title = CharField(null=True)
    description = TextField()
    company = ForeignKeyField(Company, backref="company")  # implements one to one relation
    remaining_days = CharField()


class Tag(BaseModel):
    key = CharField()
    value = CharField()
    advertisement = ForeignKeyField(Advertisement, backref="tags")
