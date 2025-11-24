"""
Flask Web Application for Caregivers Platform
Part 3: CRUD Operations Web Interface
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import (
    Base, engine, SessionLocal,
    User, Caregiver, Member, Address, Job, JobApplication, Appointment
)
from datetime import date, time, datetime
from decimal import Decimal
from sqlalchemy import or_

app = Flask(__name__)
app.secret_key = 'caregivers-platform-secret-key-2025'

# Get database session
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # Don't close here, close in routes

def close_db(db):
    db.close()


@app.route('/')
def index():
    """Home page with navigation to all tables"""
    return render_template('index.html')


# ==================== USER CRUD ====================

@app.route('/users')
def list_users():
    """List all users"""
    db = get_db()
    try:
        users = db.query(User).all()
        return render_template('users/list.html', users=users)
    finally:
        close_db(db)


@app.route('/users/create', methods=['GET', 'POST'])
def create_user():
    """Create a new user"""
    db = get_db()
    try:
        if request.method == 'POST':
            user = User(
                email=request.form['email'],
                given_name=request.form['given_name'],
                surname=request.form['surname'],
                city=request.form['city'],
                phone_number=request.form['phone_number'],
                profile_description=request.form.get('profile_description', ''),
                password=request.form['password']
            )
            db.add(user)
            db.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('list_users'))
        return render_template('users/create.html')
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
        return render_template('users/create.html')
    finally:
        close_db(db)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit an existing user"""
    db = get_db()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            flash('User not found!', 'error')
            return redirect(url_for('list_users'))
        
        if request.method == 'POST':
            user.email = request.form['email']
            user.given_name = request.form['given_name']
            user.surname = request.form['surname']
            user.city = request.form['city']
            user.phone_number = request.form['phone_number']
            user.profile_description = request.form.get('profile_description', '')
            user.password = request.form['password']
            db.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('list_users'))
        
        return render_template('users/edit.html', user=user)
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
        return render_template('users/edit.html', user=user)
    finally:
        close_db(db)


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user"""
    db = get_db()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            flash('User deleted successfully!', 'success')
        else:
            flash('User not found!', 'error')
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        close_db(db)
    return redirect(url_for('list_users'))


# ==================== CAREGIVER CRUD ====================

@app.route('/caregivers')
def list_caregivers():
    """List all caregivers"""
    db = get_db()
    try:
        caregivers = db.query(Caregiver).join(User).all()
        return render_template('caregivers/list.html', caregivers=caregivers)
    finally:
        close_db(db)


@app.route('/caregivers/create', methods=['GET', 'POST'])
def create_caregiver():
    """Create a new caregiver"""
    db = get_db()
    try:
        if request.method == 'POST':
            # First create the user
            user = User(
                email=request.form['email'],
                given_name=request.form['given_name'],
                surname=request.form['surname'],
                city=request.form['city'],
                phone_number=request.form['phone_number'],
                profile_description=request.form.get('profile_description', ''),
                password=request.form['password']
            )
            db.add(user)
            db.flush()  # Get the user_id
            
            # Then create the caregiver
            caregiver = Caregiver(
                caregiver_user_id=user.user_id,
                photo=request.form.get('photo', ''),
                gender=request.form['gender'],
                caregiving_type=request.form['caregiving_type'],
                hourly_rate=Decimal(request.form['hourly_rate'])
            )
            db.add(caregiver)
            db.commit()
            flash('Caregiver created successfully!', 'success')
            return redirect(url_for('list_caregivers'))
        
        return render_template('caregivers/create.html')
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
        return render_template('caregivers/create.html')
    finally:
        close_db(db)


@app.route('/caregivers/<int:caregiver_id>/edit', methods=['GET', 'POST'])
def edit_caregiver(caregiver_id):
    """Edit an existing caregiver"""
    db = get_db()
    try:
        caregiver = db.query(Caregiver).filter(Caregiver.caregiver_user_id == caregiver_id).first()
        if not caregiver:
            flash('Caregiver not found!', 'error')
            return redirect(url_for('list_caregivers'))
        
        if request.method == 'POST':
            caregiver.user.email = request.form['email']
            caregiver.user.given_name = request.form['given_name']
            caregiver.user.surname = request.form['surname']
            caregiver.user.city = request.form['city']
            caregiver.user.phone_number = request.form['phone_number']
            caregiver.user.profile_description = request.form.get('profile_description', '')
            caregiver.user.password = request.form['password']
            caregiver.photo = request.form.get('photo', '')
            caregiver.gender = request.form['gender']
            caregiver.caregiving_type = request.form['caregiving_type']
            caregiver.hourly_rate = Decimal(request.form['hourly_rate'])
            db.commit()
            flash('Caregiver updated successfully!', 'success')
            return redirect(url_for('list_caregivers'))
        
        return render_template('caregivers/edit.html', caregiver=caregiver)
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
        return render_template('caregivers/edit.html', caregiver=caregiver)
    finally:
        close_db(db)


@app.route('/caregivers/<int:caregiver_id>/delete', methods=['POST'])
def delete_caregiver(caregiver_id):
    """Delete a caregiver"""
    db = get_db()
    try:
        caregiver = db.query(Caregiver).filter(Caregiver.caregiver_user_id == caregiver_id).first()
        if caregiver:
            db.delete(caregiver.user)  # This will cascade delete caregiver
            db.commit()
            flash('Caregiver deleted successfully!', 'success')
        else:
            flash('Caregiver not found!', 'error')
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        close_db(db)
    return redirect(url_for('list_caregivers'))


# ==================== MEMBER CRUD ====================

@app.route('/members')
def list_members():
    """List all members"""
    db = get_db()
    try:
        members = db.query(Member).join(User).all()
        return render_template('members/list.html', members=members)
    finally:
        close_db(db)


@app.route('/members/create', methods=['GET', 'POST'])
def create_member():
    """Create a new member"""
    db = get_db()
    try:
        if request.method == 'POST':
            # First create the user
            user = User(
                email=request.form['email'],
                given_name=request.form['given_name'],
                surname=request.form['surname'],
                city=request.form['city'],
                phone_number=request.form['phone_number'],
                profile_description=request.form.get('profile_description', ''),
                password=request.form['password']
            )
            db.add(user)
            db.flush()
            
            # Then create the member
            member = Member(
                member_user_id=user.user_id,
                house_rules=request.form.get('house_rules', ''),
                dependent_description=request.form.get('dependent_description', '')
            )
            db.add(member)
            db.flush()
            
            # Create address
            address = Address(
                member_user_id=member.member_user_id,
                house_number=request.form['house_number'],
                street=request.form['street'],
                town=request.form['town']
            )
            db.add(address)
            db.commit()
            flash('Member created successfully!', 'success')
            return redirect(url_for('list_members'))
        
        return render_template('members/create.html')
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
        return render_template('members/create.html')
    finally:
        close_db(db)


@app.route('/members/<int:member_id>/edit', methods=['GET', 'POST'])
def edit_member(member_id):
    """Edit an existing member"""
    db = get_db()
    try:
        member = db.query(Member).filter(Member.member_user_id == member_id).first()
        if not member:
            flash('Member not found!', 'error')
            return redirect(url_for('list_members'))
        
        if request.method == 'POST':
            member.user.email = request.form['email']
            member.user.given_name = request.form['given_name']
            member.user.surname = request.form['surname']
            member.user.city = request.form['city']
            member.user.phone_number = request.form['phone_number']
            member.user.profile_description = request.form.get('profile_description', '')
            member.user.password = request.form['password']
            member.house_rules = request.form.get('house_rules', '')
            member.dependent_description = request.form.get('dependent_description', '')
            
            # Update address
            if member.address:
                member.address.house_number = request.form['house_number']
                member.address.street = request.form['street']
                member.address.town = request.form['town']
            
            db.commit()
            flash('Member updated successfully!', 'success')
            return redirect(url_for('list_members'))
        
        return render_template('members/edit.html', member=member)
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
        return render_template('members/edit.html', member=member)
    finally:
        close_db(db)


@app.route('/members/<int:member_id>/delete', methods=['POST'])
def delete_member(member_id):
    """Delete a member"""
    db = get_db()
    try:
        member = db.query(Member).filter(Member.member_user_id == member_id).first()
        if member:
            db.delete(member.user)  # This will cascade delete member and address
            db.commit()
            flash('Member deleted successfully!', 'success')
        else:
            flash('Member not found!', 'error')
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        close_db(db)
    return redirect(url_for('list_members'))


# ==================== JOB CRUD ====================

@app.route('/jobs')
def list_jobs():
    """List all jobs"""
    db = get_db()
    try:
        jobs = db.query(Job).join(Member).join(User).all()
        return render_template('jobs/list.html', jobs=jobs)
    finally:
        close_db(db)


@app.route('/jobs/create', methods=['GET', 'POST'])
def create_job():
    """Create a new job"""
    db = get_db()
    try:
        if request.method == 'POST':
            job = Job(
                member_user_id=int(request.form['member_user_id']),
                required_caregiving_type=request.form['required_caregiving_type'],
                other_requirements=request.form.get('other_requirements', ''),
                date_posted=datetime.strptime(request.form['date_posted'], '%Y-%m-%d').date()
            )
            db.add(job)
            db.commit()
            flash('Job created successfully!', 'success')
            return redirect(url_for('list_jobs'))
        
        members = db.query(Member).join(User).all()
        return render_template('jobs/create.html', members=members)
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
        members = db.query(Member).join(User).all()
        return render_template('jobs/create.html', members=members)
    finally:
        close_db(db)


@app.route('/jobs/<int:job_id>/edit', methods=['GET', 'POST'])
def edit_job(job_id):
    """Edit an existing job"""
    db = get_db()
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            flash('Job not found!', 'error')
            return redirect(url_for('list_jobs'))
        
        if request.method == 'POST':
            job.member_user_id = int(request.form['member_user_id'])
            job.required_caregiving_type = request.form['required_caregiving_type']
            job.other_requirements = request.form.get('other_requirements', '')
            job.date_posted = datetime.strptime(request.form['date_posted'], '%Y-%m-%d').date()
            db.commit()
            flash('Job updated successfully!', 'success')
            return redirect(url_for('list_jobs'))
        
        members = db.query(Member).join(User).all()
        return render_template('jobs/edit.html', job=job, members=members)
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
        members = db.query(Member).join(User).all()
        return render_template('jobs/edit.html', job=job, members=members)
    finally:
        close_db(db)


@app.route('/jobs/<int:job_id>/delete', methods=['POST'])
def delete_job(job_id):
    """Delete a job"""
    db = get_db()
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if job:
            db.delete(job)
            db.commit()
            flash('Job deleted successfully!', 'success')
        else:
            flash('Job not found!', 'error')
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        close_db(db)
    return redirect(url_for('list_jobs'))


# ==================== JOB APPLICATION CRUD ====================

@app.route('/job_applications')
def list_job_applications():
    """List all job applications"""
    db = get_db()
    try:
        applications = db.query(JobApplication).join(Caregiver).join(Job).all()
        return render_template('job_applications/list.html', applications=applications)
    finally:
        close_db(db)


@app.route('/job_applications/create', methods=['GET', 'POST'])
def create_job_application():
    """Create a new job application"""
    db = get_db()
    try:
        if request.method == 'POST':
            application = JobApplication(
                caregiver_user_id=int(request.form['caregiver_user_id']),
                job_id=int(request.form['job_id']),
                date_applied=datetime.strptime(request.form['date_applied'], '%Y-%m-%d').date()
            )
            db.add(application)
            db.commit()
            flash('Job application created successfully!', 'success')
            return redirect(url_for('list_job_applications'))
        
        caregivers = db.query(Caregiver).join(User).all()
        jobs = db.query(Job).all()
        return render_template('job_applications/create.html', caregivers=caregivers, jobs=jobs)
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
        caregivers = db.query(Caregiver).join(User).all()
        jobs = db.query(Job).all()
        return render_template('job_applications/create.html', caregivers=caregivers, jobs=jobs)
    finally:
        close_db(db)


@app.route('/job_applications/<int:caregiver_id>/<int:job_id>/delete', methods=['POST'])
def delete_job_application(caregiver_id, job_id):
    """Delete a job application"""
    db = get_db()
    try:
        application = db.query(JobApplication).filter(
            JobApplication.caregiver_user_id == caregiver_id,
            JobApplication.job_id == job_id
        ).first()
        if application:
            db.delete(application)
            db.commit()
            flash('Job application deleted successfully!', 'success')
        else:
            flash('Job application not found!', 'error')
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        close_db(db)
    return redirect(url_for('list_job_applications'))


# ==================== APPOINTMENT CRUD ====================

@app.route('/appointments')
def list_appointments():
    """List all appointments"""
    db = get_db()
    try:
        appointments = db.query(Appointment).join(Caregiver).join(Member).all()
        return render_template('appointments/list.html', appointments=appointments)
    finally:
        close_db(db)


@app.route('/appointments/create', methods=['GET', 'POST'])
def create_appointment():
    """Create a new appointment"""
    db = get_db()
    try:
        if request.method == 'POST':
            appointment = Appointment(
                caregiver_user_id=int(request.form['caregiver_user_id']),
                member_user_id=int(request.form['member_user_id']),
                appointment_date=datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date(),
                appointment_time=datetime.strptime(request.form['appointment_time'], '%H:%M').time(),
                work_hours=Decimal(request.form['work_hours']),
                status=request.form['status']
            )
            db.add(appointment)
            db.commit()
            flash('Appointment created successfully!', 'success')
            return redirect(url_for('list_appointments'))
        
        caregivers = db.query(Caregiver).join(User).all()
        members = db.query(Member).join(User).all()
        return render_template('appointments/create.html', caregivers=caregivers, members=members)
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
        caregivers = db.query(Caregiver).join(User).all()
        members = db.query(Member).join(User).all()
        return render_template('appointments/create.html', caregivers=caregivers, members=members)
    finally:
        close_db(db)


@app.route('/appointments/<int:appointment_id>/edit', methods=['GET', 'POST'])
def edit_appointment(appointment_id):
    """Edit an existing appointment"""
    db = get_db()
    try:
        appointment = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
        if not appointment:
            flash('Appointment not found!', 'error')
            return redirect(url_for('list_appointments'))
        
        if request.method == 'POST':
            appointment.caregiver_user_id = int(request.form['caregiver_user_id'])
            appointment.member_user_id = int(request.form['member_user_id'])
            appointment.appointment_date = datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date()
            appointment.appointment_time = datetime.strptime(request.form['appointment_time'], '%H:%M').time()
            appointment.work_hours = Decimal(request.form['work_hours'])
            appointment.status = request.form['status']
            db.commit()
            flash('Appointment updated successfully!', 'success')
            return redirect(url_for('list_appointments'))
        
        caregivers = db.query(Caregiver).join(User).all()
        members = db.query(Member).join(User).all()
        return render_template('appointments/edit.html', appointment=appointment, caregivers=caregivers, members=members)
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
        caregivers = db.query(Caregiver).join(User).all()
        members = db.query(Member).join(User).all()
        return render_template('appointments/edit.html', appointment=appointment, caregivers=caregivers, members=members)
    finally:
        close_db(db)


@app.route('/appointments/<int:appointment_id>/delete', methods=['POST'])
def delete_appointment(appointment_id):
    """Delete an appointment"""
    db = get_db()
    try:
        appointment = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
        if appointment:
            db.delete(appointment)
            db.commit()
            flash('Appointment deleted successfully!', 'success')
        else:
            flash('Appointment not found!', 'error')
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        close_db(db)
    return redirect(url_for('list_appointments'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

