#
# Project: Shopify shipping calculator
# Copyright 2014 - 2015 Esa Varemo <esa@kuivanto.fi>
# Unauthorized use or copying of this file is prohibited
#


from sqlalchemy import (
    Column,
    Integer,
    Float,
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
                                     Column('product_id', Integer, ForeignKey('products.uuid')),
                                     Column('location_id', Integer, ForeignKey('shipping_locations.uuid'))
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
    subtype = Column(Text)

    maara_per_kpl = Column(Float)

    locations = relationship('ShippingLocation',
                             secondary=product_location_assoc_table,
                             backref='products')
