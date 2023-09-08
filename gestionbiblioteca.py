

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)

    def __str__(self):
        return self.title

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = int(request.form['publication_year'])
        book = Book(title=title, author=author, publication_year=publication_year)
        db.session.add(book)
        db.session.commit()
        flash('Libro agregado con éxito.', 'success')
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        books = Book.query.filter(Book.title.contains(search_term) | Book.author.contains(search_term)).all()
        return render_template('index.html', books=books)
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
