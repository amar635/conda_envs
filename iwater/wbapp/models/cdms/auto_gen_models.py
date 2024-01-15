from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer, Numeric, String, Table, Text, text
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Designation(Base):
    __tablename__ = 'designations'

    id = Column(Integer, primary_key=True, server_default=text("nextval('designations_id_seq'::regclass)"))
    designation = Column(String, nullable=False)
    created_by = Column(String)
    created_on = Column(DateTime)


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

    code = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    created_by = Column(String)
    created_on = Column(DateTime)


class Tokenblocklist(Base):
    __tablename__ = 'tokenblocklist'

    id = Column(Integer, primary_key=True, server_default=text("nextval('tokenblocklist_id_seq'::regclass)"))
    jti = Column(String(36), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, server_default=text("nextval('users_id_seq'::regclass)"))
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    created_by = Column(String, nullable=False)
    created_on = Column(DateTime)


class District(Base):
    __tablename__ = 'districts'

    code = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    state_code = Column(ForeignKey('states.code'), nullable=False)
    created_by = Column(String)
    created_on = Column(DateTime)

    state = relationship('State')


class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True, server_default=text("nextval('participants_id_seq'::regclass)"))
    full_name = Column(String, nullable=False)
    email_address = Column(String, nullable=False, unique=True)
    mobile_number = Column(String, nullable=False, unique=True)
    gender = Column(String(10), nullable=False)
    block_name = Column(String, nullable=False)
    dept_or_org = Column(String, nullable=False)
    created_by = Column(String)
    created_on = Column(DateTime)
    designation_id = Column(ForeignKey('designations.id'), nullable=False)

    designation = relationship('Designation')


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, server_default=text("nextval('events_id_seq'::regclass)"))
    title = Column(String, nullable=False)
    venue = Column(String, nullable=False)
    address = Column(String)
    schedule = Column(DateTime, nullable=False)
    days = Column(Integer)
    mode = Column(String)
    district_code = Column(ForeignKey('districts.code'), nullable=False)
    short_url = Column(String, nullable=False, unique=True)
    created_by = Column(String)
    created_on = Column(DateTime)

    district = relationship('District')


class Attendance(Base):
    __tablename__ = 'attendances'

    id = Column(Integer, primary_key=True, server_default=text("nextval('attendances_id_seq'::regclass)"))
    event_id = Column(ForeignKey('events.id'), nullable=False)
    participant_id = Column(ForeignKey('participants.id'), nullable=False)
    attendance_date = Column(DateTime, nullable=False)
    created_by = Column(String)
    created_on = Column(DateTime)

    event = relationship('Event')
    participant = relationship('Participant')


class Feedback(Base):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True, server_default=text("nextval('feedbacks_id_seq'::regclass)"))
    rating = Column(Integer, nullable=False)
    comments = Column(String)
    participant_id = Column(ForeignKey('participants.id'), nullable=False)
    event_id = Column(ForeignKey('events.id'), nullable=False)
    created_by = Column(String)
    created_on = Column(DateTime)

    event = relationship('Event')
    participant = relationship('Participant')