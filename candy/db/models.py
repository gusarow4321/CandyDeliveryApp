import enum
from sqlalchemy import Column, Boolean, Enum, ForeignKey, Integer, Numeric, String, ARRAY, MetaData, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


class CourierType(enum.Enum):
    foot = 'foot'
    bike = 'bike'
    car = 'car'


class Courier(Base):
    __tablename__ = 'couriers'

    id = Column(Integer, primary_key=True)
    courier_type = Column(Enum(CourierType))
    regions = Column(ARRAY(Integer))
    working_hours = Column(ARRAY(String))
    rating = Column(Numeric, default=0)
    earning = Column(Integer, default=0)

    order = relationship('Order')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    weight = Column(Numeric)
    region = Column(Integer)
    delivery_hours = Column(ARRAY(String))
    assign_time = Column(DateTime)
    completed = Column(Boolean, default=False)
    completed_time = Column(DateTime)
    courier_id = Column(Integer, ForeignKey('couriers.id'))

    courier = relationship('Courier')
