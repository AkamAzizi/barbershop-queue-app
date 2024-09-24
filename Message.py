import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Website.models import QueueEntry  # Assuming the QueueEntry model includes the email field
from Website import db

def send_email(to_email, subject, body):
    from_email = "akam.azizi33@gmail.com"
    app_password = "zmii lbcc xdks dzqc"  # Use the correct app password here

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, app_password)
            server.send_message(msg)
            print(f"Email sent to {to_email} successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def notify_second_person(email):
    queue_entries = QueueEntry.query.all()

    if len(queue_entries) > 1:  # Check if there is a second person in the queue
        second_person = queue_entries[1]  # Get the second person in the queue
        
        # Check if the notification has already been sent
        if not second_person.notified:
            send_email(second_person.email, "DROP IN", "Kö-plats: 2")
            second_person.notified = True  # Update the notification status
            db.session.commit()  # Commit the change to the database
        else:
            print("Second person has already been notified.")
    else:
        print("Not enough people in the queue to notify the second person.")

def notify_first_person(email):
    queue_entries = QueueEntry.query.all()

    if len(queue_entries) > 1:  # Check if there is a second person in the queue
        first_person = queue_entries[0]  # Get the second person in the queue
        
        # Check if the notification has already been sent
        if not first_person.notified:
            send_email(first_person.email, "DROP IN", "Kö-plats: 1")
            first_person.notified = True  # Update the notification status
            db.session.commit()  # Commit the change to the database
        else:
            print("Second person has already been notified.")
    else:
        print("Not enough people in the queue to notify the second person.")

def reset_notified_status(user_email):
    entry = QueueEntry.query.filter_by(email=user_email).first()
    if entry:
        entry.notified = False  # Reset the notified status
        db.session.commit()


