from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    Table,
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship
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


product_location_assoc_table = Table('association', Base.metadata,
                                     Column('product_id', Integer, ForeignKey('product.uuid')),
                                     Column('location_id', Integer, ForeignKey('location.uuid'))
                                    )


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

    locations = relationship('ShippingLocation',
                             secondary=product_location_assoc_table,
                             backref='products')
