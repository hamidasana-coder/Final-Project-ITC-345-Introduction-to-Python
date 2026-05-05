from flask import Flask, render_template, request,url_for, redirect, session,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Book, User, History

app = Flask(__name__)


# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secretkey'
db.init_app(app) 





#-----------routes for applicatiom----------
# Login admin
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user'] = user.username
            session['user_role'] = user.role
            return redirect('/home')

        return "Invalid credentials"

    return render_template('login.html')


#home page
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')

    user = session['user']
    flash(f"Welcome {user}", "success")

    return render_template('home.html')


#--------- routes for user-----------------------------
#user homepage
@app.route('/users')
def users():
    if session.get('user_role') != 'admin':
        return "Access denied"

    page = request.args.get('page', 1, type=int)

    users = User.query.order_by(User.id.desc()).paginate(
        page=page,
        per_page=2
    )
    return render_template('users.html', users=users)

# add a new user 
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'user' not in session or session.get('user_role') != 'admin':
        return "Access denied"

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = 'user'

        #check duplicates FIRST
        existing = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()

        if existing:
            flash("Username or email already exists", "error")
            return redirect('/add_user')

        # hash password
        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            password=hashed_password,
            email=email,
            role=role,
            date_joined=db.func.current_timestamp()
        )

        db.session.add(user)
        db.session.commit()

        flash(f"{user.username} is added", "success")
        return redirect('/users')

    return render_template('add_user.html')

#edit user
@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if 'user' not in session or session.get('user_role') != 'admin':
        return "Access denied"

    user = User.query.get_or_404(id)

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        password = request.form.get('password')

        # check duplicates
        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if existing_user and existing_user.id != user.id:
            flash("Username or email already exists", "error")
            return redirect(f"/edit_user/{id}")

        user.username = username
        user.email = email
        user.role = role

        if password:
            user.password = generate_password_hash(password)

        db.session.commit()
        flash(f"updated {user.username}", "success")
        return redirect('/users')

    return render_template('edit_user.html', user=user)

#delete user
@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    if session.get('user_role') != 'admin':
        return "Access denied"

    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()
    flash(f"you removed {user.username}","success")
    return redirect('/users')


#----routes for books-----------------------
# books homepage
@app.route('/books')
def books():
    page = request.args.get('page', 1, type=int)

    books = Book.query.order_by(Book.id).paginate(
        page=page,
        per_page=2
    )

    return render_template('books.html', books=books)


# Add a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():

    if 'user' not in session or session.get('user_role') != 'admin':
        return "Access denied"

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        year = request.form.get('year')
        language = request.form.get('language')
        # duplicate check
        existing = Book.query.filter_by(title=title, author=author).first()
        if existing:
            flash("Book already exists", "error")
            return redirect('/add_book')

        new_book = Book(
            title=title,
            author=author,
            year=int(year) if year else None,
            language=language
        )
        db.session.add(new_book)
        db.session.commit()

        flash(f"{new_book.title} added", "success")
        return redirect('/books')

    return render_template('add_books.html')


# Edit a book
@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    if 'user' not in session or session.get('user_role') != 'admin':
        return "Access denied"
    book = Book.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        year = request.form.get('year')
        language = request.form.get('language')

        existing = Book.query.filter_by(title=title, author=author).first()

        if existing and existing.id != book.id:
            flash("Book already exists", "error")
            return redirect(f'/edit_book/{id}')
        
        book.title = title
        book.author=author
        book.year = int(year) if year else None
        book.language = language
        
        db.session.commit()
        flash(f"{book.title} updated", "success")
        return redirect('/books')

    return render_template('edit_book.html', book=book)



# Search for a book
@app.route('/search_book')
def search():
    query = request.args.get('q')

    if not query:
        return redirect('/books')

    results = Book.query.filter(
        Book.title.contains(query) |
        Book.author.contains(query) |
        Book.language.contains(query) |
        Book.year.contains(query)
    ).all()
    return render_template('books.html', books=results)



# Delete a book
@app.route('/delete_book/<int:id>',methods=['POST'])
def delete_book(id):
    
    if 'user' not in session:
        return redirect('/login')
    
    if session.get('user_role') != 'admin':
        return "Access denied"
    
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect('/books')


#borrow a book
@app.route('/borrow_books/<int:book_id>', methods=["GET", "POST"])
def borrow(book_id):

    if 'user' not in session or session.get('user_role') != 'admin':
        return "Access denied"
    book = Book.query.get_or_404(book_id)

    if request.method == "POST":
        username = request.form.get("username")
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("User not found", "error")
            return redirect(f"/borrow_books/{book_id}")

        if not book.available:
            flash("Book already borrowed", "error")
            return redirect("/books")

        existing = History.query.filter_by(book_id=book.id, returned_at=None).first()
        if existing:
            flash("Book already borrowed", "error")
            return redirect("/books")

        book.available = False
        record = History(user_id=user.id, book_id=book.id)
        db.session.add(record)
        db.session.commit()
        flash(f"Book assigned to {user.username}", "success")
        return redirect("/books")

    return render_template("borrow.html", book=book, users=User.query.all())



#return book
@app.route('/return_book/<int:book_id>', methods=["POST"])
def return_book(book_id):
    if 'user' not in session:
        return redirect('/login')
    book = Book.query.get_or_404(book_id)

    # allow admin to bypass ownership check
    if session.get('user_role') == 'admin':
        record = History.query.filter_by(book_id=book.id).order_by(History.id.desc()).first()
    else:
        user = User.query.filter_by(username=session['user']).first()
        record = History.query.filter_by(user_id=user.id, book_id=book.id).order_by(History.id.desc()).first()

    if not record:
        flash("No borrow record found for this book", "error")
        return redirect('/books')

    book.available = True
    db.session.delete(record)
    db.session.commit()

    flash("Book returned successfully", "success")
    return redirect('/books')



# report
@app.route('/report')
def view_borrowed_books():
    page = request.args.get('page', 1, type=int)
    records = History.query.order_by(History.id.desc()).paginate(
        page=page,
        per_page=5
    )
    return render_template('report.html', records=records)



# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_role', None)
    flash(" you logged out", "success")
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # creates tables
    app.run(debug=True)