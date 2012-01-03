from sqlalchemy.ext.declarative import declarative_base, Column
from sqlalchemy import Integer, Unicode, Text, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship


_Base = declarative_base()
DBSession = scoped_session(sessionmaker())


class BlogUser(_Base):
    """Defines a blog user"""
    __tablename__ = "blog_user"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255))
    email = Column(Unicode(255))
    date = Column(DateTime())
    entries = relationship("BlogEntry")


class BlogEntry(_Base):
    """Defines a blog entry."""
    __tablename__ = "blog_entry"
    __mapper_args__ = dict(order_by="date desc")

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('blog_user.id'))
    subject = Column(Unicode(255))
    date = Column(DateTime())
    content = Column(Text())


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    _Base.metadata.bind = engine
    _Base.metadata.create_all(engine, checkfirst=True)
