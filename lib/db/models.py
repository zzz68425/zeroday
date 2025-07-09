from typing import List, Optional

from sqlalchemy import Column, Computed, DateTime, ForeignKey, Index, Integer, Table, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime




class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = 'category'

    sn: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    domain_name: Mapped[Optional[str]] = mapped_column(Text, unique=True)

    target: Mapped[List['Target']] = relationship('Target', back_populates='category')


class Institution(Base):
    __tablename__ = 'institution'

    sn: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[str] = mapped_column(Text, unique=True)
    name: Mapped[str] = mapped_column(Text)
    domain_name: Mapped[str] = mapped_column(Text)

    target: Mapped[List['Target']] = relationship('Target', back_populates='institution')


t_latest_incident = Table(
    'latest_incident', Base.metadata,
    Column('sn', Integer),
    Column('id', Integer),
    Column('vendor', Text),
    Column('severity_sn', Integer),
    Column('vulnerability_sn', Integer),
    Column('when_start', DateTime),
    Column('when_ended', DateTime),
    Column('year_started', Integer),
    Column('duration', Integer),
    Column('when_crawled', DateTime)
)


class Severity(Base):
    __tablename__ = 'severity'

    sn: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True)

    incident: Mapped[List['Incident']] = relationship('Incident', back_populates='severity')


class Vulnerability(Base):
    __tablename__ = 'vulnerability'
    __table_args__ = (
        UniqueConstraint('name', 'description'),
    )

    sn: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)

    incident: Mapped[List['Incident']] = relationship('Incident', back_populates='vulnerability')


class Incident(Base):
    __tablename__ = 'incident'
    __table_args__ = (
        Index('incident_index_0', 'year_started'),
    )

    sn: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(Integer)
    vendor: Mapped[str] = mapped_column(Text)
    severity_sn: Mapped[int] = mapped_column(ForeignKey('severity.sn'))
    vulnerability_sn: Mapped[int] = mapped_column(ForeignKey('vulnerability.sn'))
    when_start: Mapped[datetime.datetime] = mapped_column(DateTime)
    when_ended: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    year_started: Mapped[Optional[int]] = mapped_column(Integer, Computed("STRFTIME('%Y', `when_start`)", persisted=True))
    duration: Mapped[Optional[int]] = mapped_column(
        Integer,
        Computed("""
            CASE
                WHEN `when_ended` IS NOT NULL THEN CAST(JULIANDAY(`when_ended`) - JULIANDAY(`when_start`) AS INTEGER)
                ELSE NULL
            END
        """, persisted=True)
    )
    when_crawled: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    severity: Mapped['Severity'] = relationship('Severity', back_populates='incident')
    vulnerability: Mapped['Vulnerability'] = relationship('Vulnerability', back_populates='incident')
    target: Mapped[List['Target']] = relationship('Target', back_populates='incident')


class Target(Base):
    __tablename__ = 'target'

    sn: Mapped[int] = mapped_column(Integer, primary_key=True)
    hostname: Mapped[str] = mapped_column(Text)
    category_sn: Mapped[int] = mapped_column(ForeignKey('category.sn'))
    incident_sn: Mapped[int] = mapped_column(ForeignKey('incident.sn'))
    institution_sn: Mapped[Optional[int]] = mapped_column(ForeignKey('institution.sn'))
    name: Mapped[Optional[str]] = mapped_column(Text)

    category: Mapped['Category'] = relationship('Category', back_populates='target')
    incident: Mapped['Incident'] = relationship('Incident', back_populates='target')
    institution: Mapped[Optional['Institution']] = relationship('Institution', back_populates='target')
