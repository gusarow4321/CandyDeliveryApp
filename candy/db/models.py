import enum
from sqlalchemy import Column, Boolean, Enum, ForeignKey, Integer, Numeric, String, ARRAY, MetaData
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


class Couriers(Base):
    __tablename__ = 'couriers'

    id = Column(Integer, primary_key=True)
    courier_type = Column(Enum(CourierType))
    regions = Column(ARRAY(Integer))
    working_hours = Column(ARRAY(String))
    rating = Column(Numeric)
    earning = Column(Integer)
    busy = Column(Boolean, default=False)

    order = relationship('Order')


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    weight = Column(Numeric, nullable=False)
    region = Column(Integer, nullable=False)
    delivery_hours = Column(ARRAY(String), nullable=False)
    assign_time = Column(String)
    completed = Column(Boolean, default=False)
    completed_time = Column(String)

    courier_id = Column(Integer, ForeignKey('couriers.id'))