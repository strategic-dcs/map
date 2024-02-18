import re

from sdcs.config import settings

from fastapi import Request

from sqlalchemy import create_engine, MetaData, true
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, declared_attr


class SDCSBase(object):

    @declared_attr
    def __tablename__(cls):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def get_engine():
    return create_engine(settings.DATABASE_URL, pool_pre_ping=True)


def get_session_maker(engine):
    return sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


def get_db(request: Request):
    '''
    Dependency for getting DB within calls
    '''
    return request.state.db


SQLBase = declarative_base(cls=SDCSBase, constructor=None)
