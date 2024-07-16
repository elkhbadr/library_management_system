#!/usr/bin/env python3

import sqlite3
import csv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Importez Flask-CORS

app = Flask(__name__)
CORS(app)  # Activez CORS pour votre application Flask

def connect_db():
    return sqlite3.connect('library_management.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_book')
def add_book():
    return render_template('add_book.html')

@app.route('/add_user')
def add_user():
    return render_template('add_user.html')

@app.route('/add_borrow')
def add_borrow():
    return render_template('add_borrow.html')

@app.route('/search_books')
def search_books():
    return render_template('search_books.html')

@app.route('/update_book')
def update_books():
    return render_template('update_book.html')




# Création de la table books
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        isbn TEXT DEFAULT NULL,
        isbn13 TEXT DEFAULT NULL,
        authors TEXT DEFAULT NULL,
        publication_year INTEGER DEFAULT NULL,
        title TEXT DEFAULT NULL,
        language_code TEXT DEFAULT NULL,
        average_rating REAL DEFAULT NULL,
        ratings_count INTEGER DEFAULT NULL,
        image_url TEXT DEFAULT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT DEFAULT NULL,
        last_name TEXT DEFAULT NULL,
        email TEXT DEFAULT NULL,
        phone TEXT DEFAULT NULL,
        address TEXT DEFAULT NULL,
        membership_start_date TEXT DEFAULT NULL,
        membership_end_date TEXT DEFAULT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS borrows (
        borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
        reader_id INTEGER DEFAULT NULL,
        book_id INTEGER DEFAULT NULL,
        borrow_date TEXT DEFAULT NULL,
        return_date TEXT DEFAULT NULL,
        is_returned INTEGER DEFAULT 0,
        FOREIGN KEY (reader_id) REFERENCES users (user_id),
        FOREIGN KEY (book_id) REFERENCES books (book_id) 
    );
    ''')

    conn.commit()
    conn.close()
    return jsonify({'message': 'Setup completed!'}), 201

# import data
@app.route('/data', methods=['GET','POST'])
def add_data():
    conn = connect_db()
    cursor = conn.cursor()
    # Import data from books CSV
    with open('data/books.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
            INSERT INTO books (book_id, isbn, isbn13, authors, publication_year, title, language_code, average_rating, ratings_count, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['book_id'], row['isbn'], row['isbn13'], row['authors'], 
                row['publication_year'], row['title'], row['language_code'],
                row['average_rating'], row['ratings_count'], row['image_url']
            ))
    # Import data from users CSV
    with open('data/users.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
            INSERT INTO users (user_id, first_name, last_name, email, phone, address, membership_start_date, membership_end_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['user_id'], row['first_name'], row['last_name'], row['email'], row['phone'], row['address'],
                row['membership_start_date'], row['membership_end_date']
            ))
    # Import data from borrows CSV
    with open('data/borrow.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
            INSERT INTO borrows (borrow_id, reader_id, book_id, borrow_date, return_date, is_returned)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                row['borrow_id'], row['reader_id'], row['book_id'], row['borrow_date'], row['return_date'], row['is_returned']
            ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Data imported!'}), 201




# Gestion des livres
@app.route('/books', methods=['GET', 'POST'])
def manage_books():
    conn = connect_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.get_json()
        cursor.execute('INSERT INTO books (isbn, isbn13, authors, publication_year, title, language_code, average_rating, ratings_count, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (data['isbn'],data['isbn13'], data['authors'], data['publication_year'],data['title'], data['language_code'], data['average_rating'], data['ratings_count'], data['image_url']))
        conn.commit()
        book_id = cursor.lastrowid
        return jsonify({'message': 'Book added successfully!','book_id': book_id}), 201
    
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    return render_template('add_book.html')

@app.route('/get_book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
    book = cursor.fetchone()
    conn.close()
    
    if book is None:
        return jsonify({'error': 'Book not found.'}), 404
    
    return jsonify(book), 200


# Gestion des user
@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    conn = connect_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.get_json()
        cursor.execute('INSERT INTO users (first_name, last_name, email, phone, address, membership_start_date, membership_end_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (data['first_name'], data['last_name'], data['email'], data['phone'], data['address'],
                        data['membership_start_date'], data['membership_end_date']))
        conn.commit()
        user_id = cursor.lastrowid
        return jsonify({'message': 'User added successfully!','user_id': user_id}), 201
    
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    return render_template('add_user.html')

# Gestion des emprunts
@app.route('/borrows', methods=['GET', 'POST'])
def manage_borrows():
    conn = connect_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.get_json()
        cursor.execute('INSERT INTO borrows (reader_id, book_id, borrow_date, return_date, is_returned) VALUES (?, ?, ?, ?, ?)',
                       (data['reader_id'], data['book_id'], data['borrow_date'], data['return_date'], data['is_returned']))
        conn.commit()
        borrow_id = cursor.lastrowid
        return jsonify({'message': 'Borrow added successfully!','borrow_id': borrow_id}), 201
    
    cursor.execute('SELECT * FROM borrows')
    borrows = cursor.fetchall()
    return jsonify(borrows), 200



# delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book deleted successfully!'}), 200

# update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    data = request.get_json()
    cursor.execute('''
        UPDATE users
        SET first_name = ?, last_name = ?, email = ?, phone = ?, address = ?, membership_start_date = ?, membership_end_date = ?
        WHERE user_id = ?
    ''', (
        data.get('first_name'), data.get('last_name'), data.get('email'), 
        data.get('phone'), data.get('address'), 
        data.get('membership_start_date'), data.get('membership_end_date'), 
        user_id
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User updated successfully!'}), 200

# delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User deleted successfully!'}), 200


# update a borrow
@app.route('/borrows/<int:borrow_id>', methods=['PUT'])
def update_borrow(borrow_id):
    conn = connect_db()
    cursor = conn.cursor()
    data = request.get_json()
    cursor.execute('''
        UPDATE borrows
        SET reader_id = ?, book_id = ?, borrow_date = ?, return_date = ?, is_returned = ?
        WHERE borrow_id = ?
    ''', (
        data.get('reader_id'), data.get('book_id'), 
        data.get('borrow_date'), data.get('return_date'), 
        data.get('is_returned'), borrow_id
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Borrow updated successfully!'}), 200

# delete a borrow
@app.route('/borrows/<int:borrow_id>', methods=['DELETE'])
def delete_borrow(borrow_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM borrows WHERE borrow_id = ?', (borrow_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Borrow deleted successfully!'}), 200


# search a book
@app.route('/search_books', methods=['POST'])
def search_books_api():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'A search query is required.'}), 400
    
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM books
        WHERE title LIKE ? OR authors LIKE ? OR isbn LIKE ? OR isbn13 LIKE ?
    ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
    
    books = cursor.fetchall()

    books_with_availability = []
    for book in books:
        cursor.execute('SELECT COUNT(*) FROM borrows WHERE book_id = ?', (book[0],))
        borrowed_count = cursor.fetchone()[0]
        availability = 'Available' if borrowed_count == 0 else 'Not Available'
        books_with_availability.append(book + (availability,))
    
    conn.close()
    
    return jsonify(books_with_availability), 200



# update a book
@app.route('/update_book', methods=['POST'])
def update_book():
    data = request.get_json()
    book_id = data.get('book_id')
    isbn = data.get('isbn')
    isbn13 = data.get('isbn13')
    authors = data.get('authors')
    publication_year = data.get('publication_year')
    title = data.get('title')
    language_code = data.get('language_code')
    average_rating = data.get('average_rating')
    ratings_count = data.get('ratings_count')
    image_url = data.get('image_url')

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE books
        SET isbn = ?, isbn13 = ?, authors = ?, publication_year = ?, title = ?, language_code = ?, average_rating = ?, ratings_count = ?, image_url = ?
        WHERE book_id = ?
    ''', (isbn, isbn13, authors, publication_year, title, language_code, average_rating, ratings_count, image_url, book_id))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Book updated successfully'}), 200





if __name__ == '__main__':
    app.run(debug=True)
