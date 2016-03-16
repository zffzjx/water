# coding=utf-8
from sqlalchemy import Column, String, Integer, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from handler import DBSession

Base = declarative_base()


# def session_commit():
#     try:
#         session.flush()
#         session.commit()
#     except SQLAlchemyError:
#         session.rollback()
#         raise(SQLAlchemyError)
#     finally:
#         session.close()


class TvInfo(Base):
    __tablename__ = 'tv_info'

    id = Column(Integer, primary_key=True)
    tv_id = Column(String(32))
    name = Column(String(32))
    description = Column(Text)
    last_update_time = Column(TIMESTAMP)
    update_info = Column(String(32))
    all_number = Column(String(32))
    current_number = Column(String(32))
    cast_member = Column(Text)
    platform = Column(String(32))
    label = Column(String(128))
    detail_urls = Column(Text)
    vids = Column(Text)
    type = Column(String(32))
    detail_titles = Column(Text)
    detail_episodes = Column(Text)

    @classmethod
    def add(cls, **kwds):
        session = DBSession()
        session.add(cls(**kwds))
        try:
            session.flush()
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise(SQLAlchemyError)
        finally:
            session.close()

    @classmethod
    def update(cls, **kwds):
        session = DBSession()
        session.query(cls).filter(cls.name == kwds['name']). \
            update(kwds)
        try:
            session.flush()
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise(SQLAlchemyError)
        finally:
            session.close()

    @classmethod
    def mget(cls):
        session = DBSession()
        result = session.query(cls).all()
        session.close()
        return result


class PlayInfo(Base):
    __tablename__ = 'play_info'

    id = Column(Integer, primary_key=True)
    tv_id = Column(String(32))
    tv_name = Column(String(128))
    day_play_counts = Column(String(62))
    all_play_counts = Column(String(64))
    time_at = Column(TIMESTAMP)
    platform = Column(String(32))

    @classmethod
    def mget(cls):
        session = DBSession()
        result = session.query(cls).all()
        session.close()
        return result

    @classmethod
    def add(cls, **kwds):
        session = DBSession()
        session.add(cls(**kwds))
        try:
            session.flush()
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise(SQLAlchemyError)
        finally:
            session.close()

    @classmethod
    def update(cls, **kwds):
        session = DBSession()
        session.query(cls).filter(cls.tv_id == kwds['tv_id'] and cls.tv_name
                                  == kwds['tv_name']).update(kwds)
        try:
            session.flush()
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise(SQLAlchemyError)
        finally:
            session.close()


class OpinionInfo(Base):

    __tablename__ = 'opinion_info'

    id = Column(Integer, primary_key=True)
    v_id = Column(String(32))
    like_number = Column(Integer)
    oppose_number = Column(Integer)
    tv_id = Column(String(32))
    time_at = Column(TIMESTAMP)
    comment_number = Column(Integer)
    title = Column(String(128))
    episode = Column(String(64), default='')

    @classmethod
    def mget(cls):
        session = DBSession()
        result = session.query(cls).all()
        session.close()
        return result

    @classmethod
    def add(cls, **kwds):
        session = DBSession()
        session.add(cls(**kwds))
        try:
            session.flush()
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise(SQLAlchemyError)
        finally:
            session.close()

    @classmethod
    def update(cls, **kwds):
        session = DBSession()
        session.query(cls).filter(cls.tv_id == kwds['tv_id']). \
            update(kwds)
        try:
            session.flush()
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise(SQLAlchemyError)
        finally:
            session.close()
