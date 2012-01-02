from sqlalchemy.ext.declarative import declarative_base, Column
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import scoped_session, sessionmaker
import colander


_Base = declarative_base()
DBSession = scoped_session(sessionmaker())


# XXX automate this ?
class UsersValidation(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())


class Users(_Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    _Base.metadata.bind = engine
    _Base.metadata.create_all(engine, checkfirst=True)
