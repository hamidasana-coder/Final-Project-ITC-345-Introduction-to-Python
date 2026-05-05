from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
 

#books table row
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    title = db.Column(db.String(100) )
    author = db.Column(db.String(100))
    year = db.Column(db.String(10))
    language = db.Column(db.String(50))
    available = db.Column(db.Boolean, default=True)
    history = db.relationship('History', backref='book', lazy=True)


#users table row
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    history = db.relationship('History', backref='user', lazy=True)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    date_joined = db.Column(db.DateTime, default=db.func.current_timestamp())

#history table row--to keep track of borrowed books 
class History(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    borrowed_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    returned_at = db.Column(db.DateTime, nullable=True)

