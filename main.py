from flask import Flask, render_template, request, redirect, url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

all_books = []
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-database.db'
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float(250), nullable=False)

    def __init__(self, title, author, rating):
        self.title = title
        self.author = author
        self.rating = rating


db.create_all()


@app.route('/')
def home():
    return render_template('index.html', all_books=db.session.query(Books).all())

@app.route('/delete/', methods=["GET", "POST"])
def delete():
    book_id = request.args.get('book_id')
    if request.method == "GET":
        book_to_delete = Books.query.get(book_id)
        print(book_to_delete.title)
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for('home'))
    return redirect(url_for('home'))
@app.route('/edit/<book_id>', methods=["GET", "POST"])
def edit(book_id):
    print(request.method)
    if request.method == "POST":
        print(book_id)
        new_rating = request.form['rating']
        book = Books.query.filter_by(id=book_id).first()
        book.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))
    book = Books.query.filter_by(id=book_id).first()
    print(book.title, book)
    return render_template('edit.html', book=book)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        new_dict = {key: value for (key, value) in request.form.items()}
        book_update = Books(title=new_dict['title'], author=new_dict['author'], rating=new_dict['rating'])
        all_books.append(new_dict)
        db.session.add(book_update)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)

