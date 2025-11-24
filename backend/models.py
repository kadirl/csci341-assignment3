"""
Database Models for Caregivers Platform
Shared models for both CLI and web application
"""

from sqlalchemy import create_engine, Column, Integer, String, Date, Time, DECIMAL, Text, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from decimal import Decimal
import os
import getpass

# Create base class for declarative models
Base = declarative_base()

# Database connection configuration
DB_USER = os.getenv('DB_USER', getpass.getuser())
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'caregivers_db')

# Create database connection string
if DB_PASSWORD:
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine and session factory
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


# ORM Models
class User(Base):
    __tablename__ = 'user'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    given_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    profile_description = Column(Text)
    password = Column(String(255), nullable=False)
    
    # Relationships
    caregiver = relationship("Caregiver", back_populates="user", uselist=False, cascade="all, delete-orphan")
    member = relationship("Member", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Caregiver(Base):
    __tablename__ = 'caregiver'
    
    caregiver_user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True)
    photo = Column(String(255))
    gender = Column(String(20), nullable=False)
    caregiving_type = Column(String(50), nullable=False)
    hourly_rate = Column(DECIMAL(10, 2), nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("caregiving_type IN ('babysitter', 'elderly care', 'playmate for children')", name='check_caregiving_type'),
    )
    
    # Relationships
    user = relationship("User", back_populates="caregiver")
    job_applications = relationship("JobApplication", back_populates="caregiver", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="caregiver", cascade="all, delete-orphan")


class Member(Base):
    __tablename__ = 'member'
    
    member_user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True)
    house_rules = Column(Text)
    dependent_description = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="member")
    address = relationship("Address", back_populates="member", uselist=False, cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="member", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="member", cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = 'address'
    
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), primary_key=True)
    house_number = Column(String(20), nullable=False)
    street = Column(String(255), nullable=False)
    town = Column(String(100), nullable=False)
    
    # Relationships
    member = relationship("Member", back_populates="address")


class Job(Base):
    __tablename__ = 'job'
    
    job_id = Column(Integer, primary_key=True, autoincrement=True)
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), nullable=False)
    required_caregiving_type = Column(String(50), nullable=False)
    other_requirements = Column(Text)
    date_posted = Column(Date, nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("required_caregiving_type IN ('babysitter', 'elderly care', 'playmate for children')", name='check_required_caregiving_type'),
    )
    
    # Relationships
    member = relationship("Member", back_populates="jobs")
    job_applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")


class JobApplication(Base):
    __tablename__ = 'job_application'
    
    caregiver_user_id = Column(Integer, ForeignKey('caregiver.caregiver_user_id', ondelete='CASCADE'), primary_key=True)
    job_id = Column(Integer, ForeignKey('job.job_id', ondelete='CASCADE'), primary_key=True)
    date_applied = Column(Date, nullable=False)
    
    # Relationships
    caregiver = relationship("Caregiver", back_populates="job_applications")
    job = relationship("Job", back_populates="job_applications")


class Appointment(Base):
    __tablename__ = 'appointment'
    
    appointment_id = Column(Integer, primary_key=True, autoincrement=True)
    caregiver_user_id = Column(Integer, ForeignKey('caregiver.caregiver_user_id', ondelete='CASCADE'), nullable=False)
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    work_hours = Column(DECIMAL(5, 2), nullable=False)
    status = Column(String(20), nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'accepted', 'declined')", name='check_status'),
    )
    
    # Relationships
    caregiver = relationship("Caregiver", back_populates="appointments")
    member = relationship("Member", back_populates="appointments")

