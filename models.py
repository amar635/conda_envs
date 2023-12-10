# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer, Numeric, String, Table, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Livestock(Base):
    __tablename__ = 'livestocks'

    id = Column(Integer, primary_key=True, server_default=text("nextval('livestocks_id_seq'::regclass)"))
    type = Column(String(20))
    bird_type = Column(String(30))
    name = Column(String(80), nullable=False, unique=True)
    water_use = Column(Float(53), nullable=False)


t_pg_stat_statements = Table(
    'pg_stat_statements', metadata,
    Column('userid', OID),
    Column('dbid', OID),
    Column('queryid', BigInteger),
    Column('query', Text),
    Column('plans', BigInteger),
    Column('total_plan_time', Float(53)),
    Column('min_plan_time', Float(53)),
    Column('max_plan_time', Float(53)),
    Column('mean_plan_time', Float(53)),
    Column('stddev_plan_time', Float(53)),
    Column('calls', BigInteger),
    Column('total_exec_time', Float(53)),
    Column('min_exec_time', Float(53)),
    Column('max_exec_time', Float(53)),
    Column('mean_exec_time', Float(53)),
    Column('stddev_exec_time', Float(53)),
    Column('rows', BigInteger),
    Column('shared_blks_hit', BigInteger),
    Column('shared_blks_read', BigInteger),
    Column('shared_blks_dirtied', BigInteger),
    Column('shared_blks_written', BigInteger),
    Column('local_blks_hit', BigInteger),
    Column('local_blks_read', BigInteger),
    Column('local_blks_dirtied', BigInteger),
    Column('local_blks_written', BigInteger),
    Column('temp_blks_read', BigInteger),
    Column('temp_blks_written', BigInteger),
    Column('blk_read_time', Float(53)),
    Column('blk_write_time', Float(53)),
    Column('wal_records', BigInteger),
    Column('wal_fpi', BigInteger),
    Column('wal_bytes', Numeric)
)


class State(Base):
    __tablename__ = 'states'

    id = Column(Integer, primary_key=True, server_default=text("nextval('states_id_seq'::regclass)"))
    name = Column(String(80))
    code = Column(Integer, nullable=False, unique=True)
    census_code = Column(Integer)


class District(Base):
    __tablename__ = 'districts'

    id = Column(Integer, primary_key=True, server_default=text("nextval('districts_id_seq'::regclass)"))
    name = Column(String(80), nullable=False)
    code = Column(Integer, nullable=False, unique=True)
    census_code = Column(Integer)
    state_id = Column(ForeignKey('states.id'), nullable=False)

    state = relationship('State')


class Block(Base):
    __tablename__ = 'blocks'

    id = Column(Integer, primary_key=True, server_default=text("nextval('blocks_id_seq'::regclass)"))
    name = Column(String(80))
    code = Column(Integer, nullable=False)
    census_code = Column(Integer)
    district_id = Column(ForeignKey('districts.id'), nullable=False)

    district = relationship('District')


class RainfallDatum(Base):
    __tablename__ = 'rainfall_data'

    id = Column(Integer, primary_key=True, server_default=text("nextval('rainfall_data_id_seq'::regclass)"))
    observation_date = Column(DateTime)
    normal = Column(Float(53), nullable=False)
    actual = Column(Float(53), nullable=False)
    district_id = Column(ForeignKey('districts.id'), nullable=False)

    district = relationship('District')


class Village(Base):
    __tablename__ = 'villages'
    __table_args__ = (
        UniqueConstraint('block_id', 'district_id', 'code'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('villages_id_seq'::regclass)"))
    name = Column(String(160), nullable=False)
    code = Column(Integer, nullable=False)
    census_code = Column(Integer)
    block_id = Column(ForeignKey('blocks.id'), nullable=False)
    district_id = Column(ForeignKey('districts.id'), nullable=False)

    block = relationship('Block')
    district = relationship('District')


class CensusDatum(Base):
    __tablename__ = 'census_data'

    id = Column(Integer, primary_key=True, server_default=text("nextval('census_data_id_seq'::regclass)"))
    total_geographical_area = Column(Float(53), server_default=text("0"))
    households = Column(Integer, server_default=text("0"))
    male_population = Column(Integer, server_default=text("0"))
    female_population = Column(Integer, server_default=text("0"))
    sc_population = Column(Float(53), server_default=text("0"))
    st_population = Column(Float(53), server_default=text("0"))
    forest_area = Column(Float(53), server_default=text("0"))
    non_agricultural_area = Column(Float(53), server_default=text("0"))
    uncultivable_land_area = Column(Float(53), server_default=text("0"))
    grazing_land_area = Column(Float(53), server_default=text("0"))
    misc_crops_area = Column(Float(53), server_default=text("0"))
    wasteland_area = Column(Float(53), server_default=text("0"))
    fallows_land_area = Column(Float(53), server_default=text("0"))
    current_fallows_area = Column(Float(53), server_default=text("0"))
    unirrigated_land_area = Column(Float(53), server_default=text("0"))
    canals_area = Column(Float(53), server_default=text("0"))
    tubewell_area = Column(Float(53), server_default=text("0"))
    tank_lake_area = Column(Float(53), server_default=text("0"))
    waterfall_area = Column(Float(53), server_default=text("0"))
    other_sources_area = Column(Float(53), server_default=text("0"))
    village_id = Column(ForeignKey('villages.id'), nullable=False)

    village = relationship('Village')


class LivestockCensu(Base):
    __tablename__ = 'livestock_census'
    __table_args__ = (
        UniqueConstraint('livestock_id', 'village_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('livestock_census_id_seq'::regclass)"))
    livestock_number = Column(Integer)
    livestock_id = Column(ForeignKey('livestocks.id'), nullable=False)
    village_id = Column(ForeignKey('villages.id'), nullable=False)

    livestock = relationship('Livestock')
    village = relationship('Village')


class Waterbody(Base):
    __tablename__ = 'waterbodies'

    id = Column(Integer, primary_key=True, server_default=text("nextval('waterbodies_id_seq'::regclass)"))
    waterbody_area = Column(Float(53), nullable=False)
    village_id = Column(ForeignKey('villages.id'), nullable=False)

    village = relationship('Village')
