import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Website import create_app, db
from Website.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    admin_email = 'aref@gmail.com'
    admin_user = User.query.filter_by(email=admin_email).first()

    if admin_user:
        # Update the password to be hashed
        admin_user.password = generate_password_hash('aref123', method='pbkdf2:sha256')
        db.session.commit()
        print("Admin password updated.")
    else:
        print("Admin user not found.")
