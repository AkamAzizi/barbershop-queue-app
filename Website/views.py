from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import QueueEntry  # Make sure this model exists
from . import db
from flask_login import login_required, current_user
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import User
import Message
views = Blueprint('views', __name__)

@views.route('/home', methods=['GET'])
@login_required
def home():
    queue_entries = QueueEntry.query.all()
    return render_template("home.html", user=current_user, queue_entries=queue_entries)


@views.route('/enter-queue', methods=['POST'])
@login_required
def enter_queue():
    # Check if the user is already in the queue
    existing_entry = QueueEntry.query.filter_by(customer_name=current_user.first_name).first()

    if existing_entry:
        flash('You are already in the queue.', category='warning')
    else:
        new_entry = QueueEntry(customer_name=current_user.first_name, email=current_user.email)
        db.session.add(new_entry)
        db.session.commit()
        flash('You have been added to the queue!', category='success')



    queue_entries = QueueEntry.query.order_by(QueueEntry.id).all()
        
    if len(queue_entries) > 0 and not queue_entries[0].notified:
        Message.notify_first_person(queue_entries[0].email)
        queue_entries[0].notified = True

    # Notify the second person, if there's more than 1 person in the queue, and they haven't been notified
    if len(queue_entries) > 1 and not queue_entries[1].notified:
        Message.notify_second_person(queue_entries[1].email)
        queue_entries[1].notified = True


    db.session.commit()  


    return redirect(url_for('views.home'))


@views.route('/delete-all-queue', methods=['POST'])
@login_required
def delete_all_queue():
    if not current_user.is_admin:
        flash('Access Denied. Only admins can delete entries.', category='error')
        return redirect(url_for('views.home'))

    # Delete all entries in the queue
    QueueEntry.query.delete()  # Delete all entries
    db.session.commit()  # Commit the changes
    flash('All entries in the queue have been deleted!', category='success')

    return redirect(url_for('views.home'))




@login_required
@views.route("")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))  # Redirect authenticated users to the home page
    return redirect(url_for('auth.login'))

@views.route("/delete-queue/<int:id>", methods=['POST'])
@login_required
def delete_queue(id):
    entry = QueueEntry.query.get_or_404(id)
    if not current_user.is_admin:
        flash('Access Denied. Only admins can delete entries.', category='error')
        return redirect(url_for('views.home'))
    user_mail = entry.email
    db.session.delete(entry)
    db.session.commit()
    flash('Queue entry deleted!', category='success')

    Message.reset_notified_status(user_mail)

    Message.notify_second_person(user_mail)
    Message.notify_first_person(user_mail)

    return redirect(url_for('views.home'))


@views.route('/admin/accounts', methods=['GET'])
@login_required  # Ensure the user is logged in
def admin_accounts():
    if not current_user.is_admin:
        # Redirect or raise an error if the user is not an admin
        return redirect(url_for('some_error_page'))  # Replace with your error handling
    all_users = User.query.all()  # Fetch all users
    return render_template('admin_accounts.html', users=all_users, user=current_user)

@views.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash("You do not have permission to delete users.", "error")
        return redirect(url_for('views.admin_accounts'))

    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        if user_to_delete.is_admin:
            flash("Cannot delete an admin account.", "error")
            return redirect(url_for('views.admin_accounts'))
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User account deleted successfully!", "success")
    else:
        flash("User not found.", "error")

    return redirect(url_for('views.admin_accounts'))










