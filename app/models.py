from datetime import date, datetime
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


# ===== MODELS ===== #

service_mechanics = db.Table(
    'service_mechanics',
    Base.metadata,
    Column('ticket_id', Integer, ForeignKey('service_tickets.id')),
    Column('mechanic_id', Integer, ForeignKey('mechanics.id'))
)

class Customer(Base):
    __tablename__ = 'customers'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(255), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates='customer')
    
    
class ServiceTicket(Base):
    __tablename__ = 'service_tickets'
    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(20), nullable=False)
    service_date: Mapped[str] = mapped_column(db.String(255), nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)
    
    customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
    mechanics: Mapped[List['Mechanic']] = db.relationship(secondary=service_mechanics, back_populates='service_tickets')
    service_ticket_parts: Mapped[List['ServiceTicketParts']] = db.relationship(back_populates='service_ticket')


class Mechanic(Base):
    __tablename__ = 'mechanics'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(255), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)
    
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(secondary=service_mechanics, back_populates='mechanics')
    
class Part(Base):
    __tablename__ = 'parts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    part_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float(), nullable=False)
    
    
    service_ticket_parts: Mapped[List['ServiceTicketParts']] = db.relationship(back_populates='part')
    
class ServiceTicketParts(Base):
    __tablename__ = 'service_ticket_parts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    service_ticket_id: Mapped[int] = mapped_column(db.ForeignKey('service_tickets.id'), nullable=False)
    part_id: Mapped[int] = mapped_column(db.ForeignKey('parts.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    
    service_ticket: Mapped["ServiceTicket"] = db.relationship(back_populates='service_ticket_parts')
    part: Mapped["Part"] = db.relationship(back_populates='service_ticket_parts')