from sqlalchemy import create_engine, Column, Integer, String, Date, Time, DECIMAL, Text, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import date, time, datetime
from decimal import Decimal
import os
import getpass
from pathlib import Path

Base = declarative_base()

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
    
    # relations
    caregiver = relationship(
        "Caregiver", 
        back_populates="user", 
        uselist=False, 
        cascade="all, delete-orphan")

    member = relationship(
        "Member", 
        back_populates="user", 
        uselist=False, 
        cascade="all, delete-orphan")


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
        CheckConstraint(
            "required_caregiving_type IN ('babysitter', 'elderly care', 'playmate for children')", 
            name='check_required_caregiving_type'),
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


# Database connection configuration
import getpass
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

# Create engine and session
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def create_tables():
    """
    Part 2.1: Create SQL Statements
    Create all tables according to the schema
    """
    print("=" * 80)
    print("PART 2.1: Creating Tables")
    print("=" * 80)
    
    # Drop view first if it exists (from previous runs)
    from sqlalchemy import text as sql_text
    with engine.connect() as conn:
        conn.execute(sql_text("DROP VIEW IF EXISTS job_applications_view CASCADE"))
        conn.commit()
    
    # Drop all tables if they exist
    Base.metadata.drop_all(engine)
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    print("All tables created successfully!\n")


def insert_data():
    """
    Part 2.2: Insert SQL Statements
    Insert data into appropriate tables
    """
    print("=" * 80)
    print("PART 2.2: Inserting Data")
    print("=" * 80)
    
    # Insert Users
    users_data = [
        User(email='arman.armanov@email.com', given_name='Arman', surname='Armanov', city='Astana', phone_number='+77771234567', profile_description='Experienced caregiver', password='password123'),
        User(email='amina.aminova@email.com', given_name='Amina', surname='Aminova', city='Almaty', phone_number='+77772345678', profile_description='Family member seeking care', password='password123'),
        User(email='david.davidov@email.com', given_name='David', surname='Davidov', city='Astana', phone_number='+77773456789', profile_description='Professional babysitter', password='password123'),
        User(email='elena.elenova@email.com', given_name='Elena', surname='Elenova', city='Astana', phone_number='+77774567890', profile_description='Looking for elderly care', password='password123'),
        User(email='farid.faridov@email.com', given_name='Farid', surname='Faridov', city='Almaty', phone_number='+77775678901', profile_description='Elderly care specialist', password='password123'),
        User(email='gulnara.gulnarova@email.com', given_name='Gulnara', surname='Gulnarova', city='Astana', phone_number='+77776789012', profile_description='Mother of two children', password='password123'),
        User(email='hasan.hasanov@email.com', given_name='Hasan', surname='Hasanov', city='Shymkent', phone_number='+77777890123', profile_description='Playmate for children', password='password123'),
        User(email='irina.irinova@email.com', given_name='Irina', surname='Irinova', city='Astana', phone_number='+77778901234', profile_description='Babysitter with 5 years experience', password='password123'),
        User(email='john.johnson@email.com', given_name='John', surname='Johnson', city='Almaty', phone_number='+77779012345', profile_description='Father seeking babysitter', password='password123'),
        User(email='kate.kateova@email.com', given_name='Kate', surname='Kateova', city='Astana', phone_number='+77770123456', profile_description='Elderly care professional', password='password123'),
        User(email='lisa.lisova@email.com', given_name='Lisa', surname='Lisova', city='Astana', phone_number='+77771234560', profile_description='Mother of 5-year-old son', password='password123'),
        User(email='michael.michaelov@email.com', given_name='Michael', surname='Michaelov', city='Almaty', phone_number='+77772345601', profile_description='Babysitter', password='password123'),
        User(email='nina.ninova@email.com', given_name='Nina', surname='Ninova', city='Shymkent', phone_number='+77773456712', profile_description='Family member', password='password123'),
        User(email='omar.omarov@email.com', given_name='Omar', surname='Omarov', city='Astana', phone_number='+77774567823', profile_description='Playmate specialist', password='password123'),
        User(email='paul.paulov@email.com', given_name='Paul', surname='Paulov', city='Astana', phone_number='+77775678934', profile_description='Seeking elderly care', password='password123'),
        User(email='qasim.qasimov@email.com', given_name='Qasim', surname='Qasimov', city='Almaty', phone_number='+77776789045', profile_description='Elderly care expert', password='password123'),
        User(email='rosa.rosova@email.com', given_name='Rosa', surname='Rosova', city='Astana', phone_number='+77777890156', profile_description='Babysitter', password='password123'),
        User(email='sam.samov@email.com', given_name='Sam', surname='Samov', city='Shymkent', phone_number='+77778901267', profile_description='Father of three', password='password123'),
        User(email='tina.tinova@email.com', given_name='Tina', surname='Tinova', city='Astana', phone_number='+77779012378', profile_description='Elderly care professional', password='password123'),
        User(email='umar.umarov@email.com', given_name='Umar', surname='Umarov', city='Almaty', phone_number='+77770123489', profile_description='Playmate for children', password='password123'),
    ]
    
    session.add_all(users_data)
    session.commit()
    
    # Get user IDs after commit
    users_dict = {f"{u.given_name}_{u.surname}": u.user_id for u in users_data}
    
    # Insert Caregivers
    caregivers_data = [
        Caregiver(caregiver_user_id=users_dict['Arman_Armanov'], photo='photo1.jpg', gender='Male', caregiving_type='babysitter', hourly_rate=8.50),
        Caregiver(caregiver_user_id=users_dict['David_Davidov'], photo='photo3.jpg', gender='Male', caregiving_type='babysitter', hourly_rate=9.00),
        Caregiver(caregiver_user_id=users_dict['Farid_Faridov'], photo='photo5.jpg', gender='Male', caregiving_type='elderly care', hourly_rate=12.00),
        Caregiver(caregiver_user_id=users_dict['Hasan_Hasanov'], photo='photo7.jpg', gender='Male', caregiving_type='playmate for children', hourly_rate=7.50),
        Caregiver(caregiver_user_id=users_dict['Irina_Irinova'], photo='photo8.jpg', gender='Female', caregiving_type='babysitter', hourly_rate=10.00),
        Caregiver(caregiver_user_id=users_dict['Kate_Kateova'], photo='photo10.jpg', gender='Female', caregiving_type='elderly care', hourly_rate=11.50),
        Caregiver(caregiver_user_id=users_dict['Michael_Michaelov'], photo='photo12.jpg', gender='Male', caregiving_type='babysitter', hourly_rate=9.50),
        Caregiver(caregiver_user_id=users_dict['Omar_Omarov'], photo='photo14.jpg', gender='Male', caregiving_type='playmate for children', hourly_rate=8.00),
        Caregiver(caregiver_user_id=users_dict['Rosa_Rosova'], photo='photo17.jpg', gender='Female', caregiving_type='babysitter', hourly_rate=10.50),
        Caregiver(caregiver_user_id=users_dict['Tina_Tinova'], photo='photo19.jpg', gender='Female', caregiving_type='elderly care', hourly_rate=13.00),
        Caregiver(caregiver_user_id=users_dict['Umar_Umarov'], photo='photo20.jpg', gender='Male', caregiving_type='playmate for children', hourly_rate=7.00),
    ]
    
    session.add_all(caregivers_data)
    session.commit()
    
    # Insert Members
    members_data = [
        Member(member_user_id=users_dict['Amina_Aminova'], house_rules='No pets. Please maintain hygiene.', dependent_description='Looking for babysitter for 3-year-old daughter'),
        Member(member_user_id=users_dict['Elena_Elenova'], house_rules='No pets. Quiet environment required.', dependent_description='Elderly mother needs daily care, age 75'),
        Member(member_user_id=users_dict['Gulnara_Gulnarova'], house_rules='No pets. Clean environment.', dependent_description='I have a 5-year-old son who likes painting'),
        Member(member_user_id=users_dict['John_Johnson'], house_rules='Pets allowed. Respectful behavior.', dependent_description='Two children aged 4 and 6 need babysitting'),
        Member(member_user_id=users_dict['Lisa_Lisova'], house_rules='No pets. Strict hygiene rules.', dependent_description='5-year-old son who likes painting and drawing'),
        Member(member_user_id=users_dict['Nina_Ninova'], house_rules='No pets. Professional care required.', dependent_description='Elderly father, age 80, needs assistance'),
        Member(member_user_id=users_dict['Paul_Paulov'], house_rules='No pets. Regular schedule.', dependent_description='Elderly grandmother, age 70, needs care'),
        Member(member_user_id=users_dict['Qasim_Qasimov'], house_rules='No pets. Soft-spoken caregiver preferred.', dependent_description='Elderly parent needs gentle care'),
        Member(member_user_id=users_dict['Sam_Samov'], house_rules='Pets allowed. Flexible schedule.', dependent_description='Three children need playmate and supervision'),
    ]
    
    session.add_all(members_data)
    session.commit()
    
    # Insert Addresses
    addresses_data = [
        Address(member_user_id=users_dict['Amina_Aminova'], house_number='15', street='Kabanbay Batyr', town='Astana'),
        Address(member_user_id=users_dict['Elena_Elenova'], house_number='22', street='Abay Avenue', town='Astana'),
        Address(member_user_id=users_dict['Gulnara_Gulnarova'], house_number='33', street='Kabanbay Batyr', town='Astana'),
        Address(member_user_id=users_dict['John_Johnson'], house_number='44', street='Al-Farabi Avenue', town='Almaty'),
        Address(member_user_id=users_dict['Lisa_Lisova'], house_number='55', street='Kabanbay Batyr', town='Astana'),
        Address(member_user_id=users_dict['Nina_Ninova'], house_number='66', street='Tauelsizdik Avenue', town='Shymkent'),
        Address(member_user_id=users_dict['Paul_Paulov'], house_number='77', street='Kabanbay Batyr', town='Astana'),
        Address(member_user_id=users_dict['Qasim_Qasimov'], house_number='88', street='Abay Avenue', town='Astana'),
        Address(member_user_id=users_dict['Sam_Samov'], house_number='99', street='Al-Farabi Avenue', town='Almaty'),
    ]
    
    session.add_all(addresses_data)
    session.commit()
    
    # Insert Jobs
    jobs_data = [
        Job(member_user_id=users_dict['Amina_Aminova'], required_caregiving_type='babysitter', other_requirements='Must be soft-spoken and patient', date_posted=date(2025, 1, 15)),
        Job(member_user_id=users_dict['Elena_Elenova'], required_caregiving_type='elderly care', other_requirements='Experience with dementia patients preferred', date_posted=date(2025, 1, 16)),
        Job(member_user_id=users_dict['Gulnara_Gulnarova'], required_caregiving_type='babysitter', other_requirements='Art background preferred, soft-spoken', date_posted=date(2025, 1, 17)),
        Job(member_user_id=users_dict['John_Johnson'], required_caregiving_type='babysitter', other_requirements='Energetic and fun-loving', date_posted=date(2025, 1, 18)),
        Job(member_user_id=users_dict['Lisa_Lisova'], required_caregiving_type='playmate for children', other_requirements='Creative activities required', date_posted=date(2025, 1, 19)),
        Job(member_user_id=users_dict['Nina_Ninova'], required_caregiving_type='elderly care', other_requirements='Medical training preferred', date_posted=date(2025, 1, 20)),
        Job(member_user_id=users_dict['Paul_Paulov'], required_caregiving_type='elderly care', other_requirements='Gentle and caring personality', date_posted=date(2025, 1, 21)),
        Job(member_user_id=users_dict['Qasim_Qasimov'], required_caregiving_type='elderly care', other_requirements='Soft-spoken caregiver needed', date_posted=date(2025, 1, 22)),
        Job(member_user_id=users_dict['Sam_Samov'], required_caregiving_type='playmate for children', other_requirements='Active and engaging', date_posted=date(2025, 1, 23)),
        Job(member_user_id=users_dict['Amina_Aminova'], required_caregiving_type='babysitter', other_requirements='Weekend availability required', date_posted=date(2025, 1, 24)),
        Job(member_user_id=users_dict['Elena_Elenova'], required_caregiving_type='elderly care', other_requirements='Morning shifts preferred', date_posted=date(2025, 1, 25)),
        Job(member_user_id=users_dict['Gulnara_Gulnarova'], required_caregiving_type='babysitter', other_requirements='Afternoon availability', date_posted=date(2025, 1, 26)),
        Job(member_user_id=users_dict['John_Johnson'], required_caregiving_type='playmate for children', other_requirements='Outdoor activities preferred', date_posted=date(2025, 1, 27)),
        Job(member_user_id=users_dict['Lisa_Lisova'], required_caregiving_type='babysitter', other_requirements='Educational activities', date_posted=date(2025, 1, 28)),
        Job(member_user_id=users_dict['Nina_Ninova'], required_caregiving_type='elderly care', other_requirements='Evening care needed', date_posted=date(2025, 1, 29)),
    ]
    
    session.add_all(jobs_data)
    session.commit()
    
    # Get job IDs after commit
    jobs_list = session.query(Job).order_by(Job.job_id).all()
    
    # Insert Job Applications
    job_applications_data = [
        JobApplication(caregiver_user_id=users_dict['Arman_Armanov'], job_id=jobs_list[0].job_id, date_applied=date(2025, 1, 20)),
        JobApplication(caregiver_user_id=users_dict['David_Davidov'], job_id=jobs_list[0].job_id, date_applied=date(2025, 1, 21)),
        JobApplication(caregiver_user_id=users_dict['Irina_Irinova'], job_id=jobs_list[0].job_id, date_applied=date(2025, 1, 22)),
        JobApplication(caregiver_user_id=users_dict['Arman_Armanov'], job_id=jobs_list[1].job_id, date_applied=date(2025, 1, 25)),
        JobApplication(caregiver_user_id=users_dict['Farid_Faridov'], job_id=jobs_list[1].job_id, date_applied=date(2025, 1, 26)),
        JobApplication(caregiver_user_id=users_dict['Kate_Kateova'], job_id=jobs_list[1].job_id, date_applied=date(2025, 1, 27)),
        JobApplication(caregiver_user_id=users_dict['Tina_Tinova'], job_id=jobs_list[1].job_id, date_applied=date(2025, 1, 28)),
        JobApplication(caregiver_user_id=users_dict['Arman_Armanov'], job_id=jobs_list[2].job_id, date_applied=date(2025, 1, 30)),
        JobApplication(caregiver_user_id=users_dict['Irina_Irinova'], job_id=jobs_list[2].job_id, date_applied=date(2025, 1, 31)),
        JobApplication(caregiver_user_id=users_dict['Michael_Michaelov'], job_id=jobs_list[2].job_id, date_applied=date(2025, 2, 1)),
        JobApplication(caregiver_user_id=users_dict['Rosa_Rosova'], job_id=jobs_list[2].job_id, date_applied=date(2025, 2, 2)),
        JobApplication(caregiver_user_id=users_dict['Hasan_Hasanov'], job_id=jobs_list[4].job_id, date_applied=date(2025, 2, 3)),
        JobApplication(caregiver_user_id=users_dict['Omar_Omarov'], job_id=jobs_list[4].job_id, date_applied=date(2025, 2, 4)),
        JobApplication(caregiver_user_id=users_dict['Umar_Umarov'], job_id=jobs_list[4].job_id, date_applied=date(2025, 2, 5)),
        JobApplication(caregiver_user_id=users_dict['Farid_Faridov'], job_id=jobs_list[5].job_id, date_applied=date(2025, 2, 6)),
        JobApplication(caregiver_user_id=users_dict['Kate_Kateova'], job_id=jobs_list[5].job_id, date_applied=date(2025, 2, 7)),
        JobApplication(caregiver_user_id=users_dict['Tina_Tinova'], job_id=jobs_list[5].job_id, date_applied=date(2025, 2, 8)),
        JobApplication(caregiver_user_id=users_dict['Farid_Faridov'], job_id=jobs_list[6].job_id, date_applied=date(2025, 2, 9)),
        JobApplication(caregiver_user_id=users_dict['Kate_Kateova'], job_id=jobs_list[6].job_id, date_applied=date(2025, 2, 10)),
        JobApplication(caregiver_user_id=users_dict['Tina_Tinova'], job_id=jobs_list[6].job_id, date_applied=date(2025, 2, 11)),
        JobApplication(caregiver_user_id=users_dict['Farid_Faridov'], job_id=jobs_list[7].job_id, date_applied=date(2025, 2, 12)),
        JobApplication(caregiver_user_id=users_dict['Kate_Kateova'], job_id=jobs_list[7].job_id, date_applied=date(2025, 2, 13)),
        JobApplication(caregiver_user_id=users_dict['Tina_Tinova'], job_id=jobs_list[7].job_id, date_applied=date(2025, 2, 14)),
        JobApplication(caregiver_user_id=users_dict['Hasan_Hasanov'], job_id=jobs_list[8].job_id, date_applied=date(2025, 2, 15)),
        JobApplication(caregiver_user_id=users_dict['Omar_Omarov'], job_id=jobs_list[8].job_id, date_applied=date(2025, 2, 16)),
        JobApplication(caregiver_user_id=users_dict['Umar_Umarov'], job_id=jobs_list[8].job_id, date_applied=date(2025, 2, 17)),
    ]
    
    session.add_all(job_applications_data)
    session.commit()
    
    # Insert Appointments
    appointments_data = [
        Appointment(caregiver_user_id=users_dict['Arman_Armanov'], member_user_id=users_dict['Amina_Aminova'], appointment_date=date(2025, 2, 10), appointment_time=time(9, 0), work_hours=3.0, status='accepted'),
        Appointment(caregiver_user_id=users_dict['David_Davidov'], member_user_id=users_dict['Gulnara_Gulnarova'], appointment_date=date(2025, 2, 11), appointment_time=time(14, 0), work_hours=4.0, status='accepted'),
        Appointment(caregiver_user_id=users_dict['Farid_Faridov'], member_user_id=users_dict['Elena_Elenova'], appointment_date=date(2025, 2, 12), appointment_time=time(10, 0), work_hours=5.0, status='accepted'),
        Appointment(caregiver_user_id=users_dict['Irina_Irinova'], member_user_id=users_dict['John_Johnson'], appointment_date=date(2025, 2, 13), appointment_time=time(15, 0), work_hours=3.5, status='accepted'),
        Appointment(caregiver_user_id=users_dict['Kate_Kateova'], member_user_id=users_dict['Nina_Ninova'], appointment_date=date(2025, 2, 14), appointment_time=time(8, 0), work_hours=6.0, status='accepted'),
        Appointment(caregiver_user_id=users_dict['Michael_Michaelov'], member_user_id=users_dict['Lisa_Lisova'], appointment_date=date(2025, 2, 15), appointment_time=time(16, 0), work_hours=2.5, status='accepted'),
        Appointment(caregiver_user_id=users_dict['Rosa_Rosova'], member_user_id=users_dict['Sam_Samov'], appointment_date=date(2025, 2, 16), appointment_time=time(11, 0), work_hours=4.0, status='accepted'),
        Appointment(caregiver_user_id=users_dict['Tina_Tinova'], member_user_id=users_dict['Paul_Paulov'], appointment_date=date(2025, 2, 17), appointment_time=time(9, 30), work_hours=5.5, status='accepted'),
        Appointment(caregiver_user_id=users_dict['Arman_Armanov'], member_user_id=users_dict['Gulnara_Gulnarova'], appointment_date=date(2025, 2, 18), appointment_time=time(13, 0), work_hours=3.0, status='accepted'),
        Appointment(caregiver_user_id=users_dict['Farid_Faridov'], member_user_id=users_dict['Qasim_Qasimov'], appointment_date=date(2025, 2, 19), appointment_time=time(10, 0), work_hours=4.0, status='accepted'),
        Appointment(caregiver_user_id=users_dict['Irina_Irinova'], member_user_id=users_dict['Amina_Aminova'], appointment_date=date(2025, 2, 20), appointment_time=time(14, 0), work_hours=3.0, status='pending'),
        Appointment(caregiver_user_id=users_dict['Kate_Kateova'], member_user_id=users_dict['Elena_Elenova'], appointment_date=date(2025, 2, 21), appointment_time=time(11, 0), work_hours=4.0, status='pending'),
        Appointment(caregiver_user_id=users_dict['David_Davidov'], member_user_id=users_dict['John_Johnson'], appointment_date=date(2025, 2, 22), appointment_time=time(15, 0), work_hours=2.0, status='declined'),
        Appointment(caregiver_user_id=users_dict['Hasan_Hasanov'], member_user_id=users_dict['Lisa_Lisova'], appointment_date=date(2025, 2, 23), appointment_time=time(16, 0), work_hours=3.0, status='pending'),
        Appointment(caregiver_user_id=users_dict['Omar_Omarov'], member_user_id=users_dict['Sam_Samov'], appointment_date=date(2025, 2, 24), appointment_time=time(12, 0), work_hours=4.0, status='declined'),
    ]
    
    session.add_all(appointments_data)
    session.commit()
    
    print("Data inserted successfully!\n")


def update_queries():
    """
    Part 2.3: Update SQL Statements
    """
    print("=" * 80)
    print("PART 2.3: Update SQL Statements")
    print("=" * 80)
    
    # 3.1 Update the phone number of Arman Armanov to +77773414141
    print("3.1: Update phone number of Arman Armanov to +77773414141")
    user = session.query(User).filter(User.given_name == 'Arman', User.surname == 'Armanov').first()
    if user:
        user.phone_number = '+77773414141'
        session.commit()
        print(f"Rows updated: 1\n")
    else:
        print("User not found\n")
    
    # 3.2 Add $0.3 commission fee to the Caregivers' hourly rate if it's less than $10, or 10% if it's not
    print("3.2: Add commission fee to Caregivers' hourly rate")
    print("  - If hourly_rate < $10: add $0.3")
    print("  - If hourly_rate >= $10: add 10%")
    caregivers = session.query(Caregiver).all()
    updated_count = 0
    for caregiver in caregivers:
        if caregiver.hourly_rate < Decimal('10'):
            caregiver.hourly_rate = caregiver.hourly_rate + Decimal('0.3')
        else:
            caregiver.hourly_rate = caregiver.hourly_rate * Decimal('1.10')
        updated_count += 1
    session.commit()
    print(f"Rows updated: {updated_count}\n")


def delete_queries():
    """
    Part 2.4: Delete SQL Statements
    """
    print("=" * 80)
    print("PART 2.4: Delete SQL Statements")
    print("=" * 80)
    
    # 4.1 Delete the jobs posted by Amina Aminova
    print("4.1: Delete jobs posted by Amina Aminova")
    member = session.query(Member).join(User).filter(User.given_name == 'Amina', User.surname == 'Aminova').first()
    if member:
        deleted_count = len(member.jobs)
        for job in member.jobs:
            session.delete(job)
        session.commit()
        print(f"Rows deleted: {deleted_count}\n")
    else:
        print("Member not found\n")
    
    # 4.2 Delete all members who live on Kabanbay Batyr street
    print("4.2: Delete all members who live on Kabanbay Batyr street")
    addresses = session.query(Address).filter(Address.street == 'Kabanbay Batyr').all()
    deleted_count = 0
    for address in addresses:
        if address.member:
            session.delete(address.member)
            deleted_count += 1
    session.commit()
    print(f"Rows deleted: {deleted_count}\n")


def simple_queries():
    """
    Part 2.5: Simple Queries
    """
    print("=" * 80)
    print("PART 2.5: Simple Queries")
    print("=" * 80)
    
    # 5.1 Select caregiver and member names for the accepted appointments
    print("5.1: Select caregiver and member names for the accepted appointments")
    appointments = session.query(Appointment).filter(Appointment.status == 'accepted').all()
    for apt in appointments:
        caregiver_name = f"{apt.caregiver.user.given_name} {apt.caregiver.user.surname}"
        member_name = f"{apt.member.user.given_name} {apt.member.user.surname}"
        print(f"  Caregiver: {caregiver_name}, Member: {member_name}")
    print(f"Total rows: {len(appointments)}\n")
    
    # 5.2 List job ids that contain 'soft-spoken' in their other requirements
    print("5.2: List job ids that contain 'soft-spoken' in their other requirements")
    jobs = session.query(Job).filter(Job.other_requirements.contains('soft-spoken')).all()
    for job in jobs:
        print(f"  Job ID: {job.job_id}")
    print(f"Total rows: {len(jobs)}\n")
    
    # 5.3 List the work hours of all babysitter positions
    print("5.3: List the work hours of all babysitter positions")
    appointments = session.query(Appointment).join(Caregiver).filter(Caregiver.caregiving_type == 'babysitter').all()
    for apt in appointments:
        print(f"  Work hours: {apt.work_hours}")
    print(f"Total rows: {len(appointments)}\n")
    
    # 5.4 List the members who are looking for Elderly Care in Astana and have "No pets." rule
    print("5.4: List members looking for Elderly Care in Astana with 'No pets.' rule")
    members = session.query(Member).join(User).join(Job).filter(
        Job.required_caregiving_type == 'elderly care',
        User.city == 'Astana',
        Member.house_rules.contains('No pets.')
    ).distinct().all()
    for member in members:
        member_name = f"{member.user.given_name} {member.user.surname}"
        print(f"  Member: {member_name}")
    print(f"Total rows: {len(members)}\n")


def complex_queries():
    """
    Part 2.6: Complex Queries
    """
    print("=" * 80)
    print("PART 2.6: Complex Queries")
    print("=" * 80)
    
    # 6.1 Count the number of applicants for each job posted by a member
    print("6.1: Count the number of applicants for each job posted by a member")
    jobs = session.query(Job).all()
    for job in jobs:
        applicant_count = len(job.job_applications)
        member_name = f"{job.member.user.given_name} {job.member.user.surname}"
        print(f"  Job ID: {job.job_id}, Member: {member_name}, Applicants: {applicant_count}")
    print(f"Total rows: {len(jobs)}\n")
    
    # 6.2 Total hours spent by caregivers for all accepted appointments
    print("6.2: Total hours spent by caregivers for all accepted appointments")
    total_hours = session.query(func.sum(Appointment.work_hours)).filter(Appointment.status == 'accepted').scalar()
    total_hours = total_hours if total_hours is not None else 0
    print(f"  Total hours: {total_hours}\n")
    
    # 6.3 Average pay of caregivers based on accepted appointments
    print("6.3: Average pay of caregivers based on accepted appointments")
    avg_pay = session.query(func.avg(Caregiver.hourly_rate * Appointment.work_hours)).join(
        Appointment, Caregiver.caregiver_user_id == Appointment.caregiver_user_id
    ).filter(Appointment.status == 'accepted').scalar()
    avg_pay = avg_pay if avg_pay is not None else 0.0
    print(f"  Average pay: ${avg_pay:.2f}\n")
    
    # 6.4 Caregivers who earn above average based on accepted appointments
    print("6.4: Caregivers who earn above average based on accepted appointments")
    # First calculate average
    avg_earnings = session.query(func.avg(Caregiver.hourly_rate * Appointment.work_hours)).join(
        Appointment, Caregiver.caregiver_user_id == Appointment.caregiver_user_id
    ).filter(Appointment.status == 'accepted').scalar()
    
    if avg_earnings is not None:
        # Then find caregivers above average
        results = session.query(
            User.given_name + ' ' + User.surname,
            func.sum(Caregiver.hourly_rate * Appointment.work_hours)
        ).join(Caregiver, User.user_id == Caregiver.caregiver_user_id).join(
            Appointment, Caregiver.caregiver_user_id == Appointment.caregiver_user_id
        ).filter(Appointment.status == 'accepted').group_by(
            User.given_name, User.surname
        ).having(
            func.sum(Caregiver.hourly_rate * Appointment.work_hours) > avg_earnings
        ).order_by(func.sum(Caregiver.hourly_rate * Appointment.work_hours).desc()).all()
        
        if len(results) == 0:
            print("  No caregivers found earning above average (or no accepted appointments exist).\n")
        else:
            for row in results:
                print(f"  Caregiver: {row[0]}, Total Earnings: ${row[1]:.2f}")
            print(f"Total rows: {len(results)}\n")
    else:
        print("  No accepted appointments found.\n")


def derived_attribute_query():
    """
    Part 2.7: Query with a Derived Attribute
    """
    print("=" * 80)
    print("PART 2.7: Query with a Derived Attribute")
    print("=" * 80)
    
    # Calculate the total cost to pay for a caregiver for all accepted appointments
    print("Calculate total cost to pay for caregivers for all accepted appointments")
    appointments = session.query(Appointment).join(Caregiver).join(User).filter(
        Appointment.status == 'accepted'
    ).all()
    
    if len(appointments) == 0:
        print("  No accepted appointments found.\n")
    else:
        total_sum = 0
        for apt in appointments:
            caregiver_name = f"{apt.caregiver.user.given_name} {apt.caregiver.user.surname}"
            total_cost = float(apt.caregiver.hourly_rate * apt.work_hours)
            print(f"  Appointment {apt.appointment_id}: {caregiver_name} - ${apt.caregiver.hourly_rate:.2f}/hr × {apt.work_hours} hrs = ${total_cost:.2f}")
            total_sum += total_cost
        print(f"\n  Grand Total: ${total_sum:.2f}\n")


def view_operation():
    """
    Part 2.8: View Operation
    """
    print("=" * 80)
    print("PART 2.8: View Operation")
    print("=" * 80)
    
    # Create view for job applications and applicants
    print("Creating view: job_applications_view")
    from sqlalchemy import text as sql_text
    
    with engine.connect() as conn:
        # Drop view if exists
        conn.execute(sql_text("DROP VIEW IF EXISTS job_applications_view"))
        conn.commit()
        
        # Create view
        conn.execute(sql_text("""
            CREATE VIEW job_applications_view AS
            SELECT 
                ja.job_id,
                j.required_caregiving_type,
                j.other_requirements,
                j.date_posted,
                ja.caregiver_user_id,
                u.given_name || ' ' || u.surname AS applicant_name,
                c.caregiving_type,
                c.hourly_rate,
                ja.date_applied
            FROM job_application ja
            JOIN job j ON ja.job_id = j.job_id
            JOIN caregiver c ON ja.caregiver_user_id = c.caregiver_user_id
            JOIN "user" u ON c.caregiver_user_id = u.user_id
        """))
        conn.commit()
        print("View created successfully!\n")
    
    # Query the view using ORM (we'll use raw SQL for the view since it's a view)
    print("Querying the view:")
    with engine.connect() as conn:
        result = conn.execute(sql_text("SELECT * FROM job_applications_view ORDER BY job_id, date_applied"))
        rows = result.fetchall()
        for row in rows:
            print(f"  Job {row[0]}: {row[5]} applied for {row[1]} position on {row[8]}")
        print(f"Total rows: {len(rows)}\n")


def main():
    """
    Main function to execute all database operations
    """
    print("\n" + "=" * 80)
    print("CSCI 341 Assignment 3 - Part 2")
    print("Database Operations using SQLAlchemy ORM")
    print("=" * 80 + "\n")
    
    try:
        # Part 2.1: Create tables
        create_tables()
        
        # Part 2.2: Insert data
        insert_data()
        
        # Part 2.3: Update queries
        update_queries()
        
        # Part 2.4: Delete queries
        delete_queries()
        
        # Part 2.5: Simple queries
        simple_queries()
        
        # Part 2.6: Complex queries
        complex_queries()
        
        # Part 2.7: Query with derived attribute
        derived_attribute_query()
        
        # Part 2.8: View operation
        view_operation()
        
        print("=" * 80)
        print("All operations completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    main()
