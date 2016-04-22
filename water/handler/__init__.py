# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://cg:123456@localhost:3306/water?charset=utf8&unix_socket=/var/mysql/data/mysql.sock', echo=False) # noqa
DBSession = sessionmaker(bind=engine)
