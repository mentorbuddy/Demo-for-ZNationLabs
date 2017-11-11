# app/admin/views.py

from flask import abort, flash, redirect, url_for, render_template
from flask_login import current_user, login_required

from . import admin
from .forms import DepartmentForm, MenteeAssignForm, MentorForm
from ..models import Department, Mentee, Mentor
from .. import db

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        print ("Not admin detected")
        abort(403)

# Department Views

@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")

@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")

@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")

@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")

# Mentor Views

@admin.route('/mentors')
@login_required
def list_mentors():
    check_admin()
    """
    List all mentors
    """
    mentors = Mentor.query.all()
    return render_template('admin/mentor/mentors.html',
                           mentors=mentors, title='Mentors')
    #return("Hello World")


@admin.route('/mentors/add', methods=['GET', 'POST'])
@login_required
def add_mentor():
    """
    Add a mentor to the database
    """
    check_admin()

    add_mentor = True

    form = MentorForm()
    if form.validate_on_submit():
        mentor = Mentor(name=form.name.data,
                    description=form.description.data)

        try:
            # add mentor to the database
            db.session.add(mentor)
            db.session.commit()
            flash('You have successfully added a new mentor.')
        except:
            # in case mentor name already exists
            flash('Error: mentor name already exists.')

        # redirect to the mentors page
        return redirect(url_for('admin.list_mentors'))

    # load mentor template
    return render_template('admin/mentors/mentor.html', add_mentor=add_mentor,
                           form=form, title='Add Mentor')

@admin.route('/mentors/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_mentor(id):
    """
    Edit a mentor
    """
    check_admin()

    add_mentor = False

    mentor = Mentor.query.get_or_404(id)
    form = MentorForm(obj=mentor)
    if form.validate_on_submit():
        mentor.name = form.name.data
        mentor.description = form.description.data
        db.session.add(mentor)
        db.session.commit()
        flash('You have successfully edited the mentor.')

        # redirect to the mentors page
        return redirect(url_for('admin.list_mentors'))

    form.description.data = mentor.description
    form.name.data = mentor.name
    return render_template('admin/mentors/mentor.html', add_mentor=add_mentor,
                           form=form, title="Edit mentor")

@admin.route('/mentors/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_mentor(id):
    """
    Delete a mentor from the database
    """
    check_admin()

    mentor = Mentor.query.get_or_404(id)
    db.session.delete(mentor)
    db.session.commit()
    flash('You have successfully deleted the mentor.')

    # redirect to the mentors page
    return redirect(url_for('admin.list_mentors'))

    return render_template(title="Delete Mentor")

# Mentee Views

@admin.route('/mentees')
@login_required
def list_mentees():
    """
    List all mentees
    """
    check_admin()

    mentees = Mentee.query.all()
    return render_template('admin/mentees/mentees.html',
                           mentees=mentees, title='Mentees')

@admin.route('/mentees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_mentee(id):
    """
    Assign a department and a mentor to an mentee
    """
    check_admin()

    mentee = Mentee.query.get_or_404(id)

    # prevent admin from being assigned a department or mentor
    if Mentee.is_admin:
        abort(403)

    form = MenteeAssignForm(obj=mentee)
    if form.validate_on_submit():
        mentee.department = form.department.data
        mentee.mentor = form.mentor.data
        db.session.add(mentee)
        db.session.commit()
        flash('You have successfully assigned a department and mentor.')

        # redirect to the mentors page
        return redirect(url_for('admin.list_mentees'))

    return render_template('admin/mentees/mentee.html',
                           mentee=mentee, form=form,
                           title='Assign Mentee')