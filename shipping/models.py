from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class QuoteRequest(Base):
    """
    A database model used for storing requests made to the
    callback by shopify for later inspection and testing
    """
    __tablename__ = 'requests'
    uuid = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)

    json = Column(Text) # Stores json-formated request body from shopify


class ShippingLocation(Base):
    __tablename__ = 'shipping_locations'
    uuid = Column(Integer, primary_key=True)

    name = Column(Text)
    address = Column(Text)

class Product(Base):
    __tablename__ = 'products'
    uuid = Column(Integer, primary_key=True)

    handle = Column(Text)
    type = Column(Text)
