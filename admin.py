# here is  a maunall admin input and creation file to create admin user in database
#and the rest users would be created by registration form in the app.py
#  file with user role as user by default

from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User(
        username='admin',
        password=generate_password_hash('admin123'),
        email='admin@email.com',
        role='admin'
    )

    db.session.add(admin)
    db.session.commit()

    print("Admin created")