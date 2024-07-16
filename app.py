#!/usr/bin/env python3

import sqlite3
import csv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import Flask-CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask application

# Function to connect to SQLite database
def connect_db():
    return sqlite3.connect('library_management.db')

# Route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Route to render the add_book.html template
@app.route('/add_book')
def add_book():
    return render_template('add_book.html')

# Route to render the add_user.html template
@app.route('/add_user')
def add_user():
    return render_template('add_user.html')

# Route to render the add_borrow.html template
@app.route('/add_borrow')
def add_borrow():
    return render_template('add_borrow.html')

# Route to render the search_books.html template
@app.route('/search_books')
def search_books():
    return render_template('search_books.html')

# Route to render the update_book.html template
@app.route('/update_book')
def update_books():
    return render_template('update_book.html')

# Create the 'books', 'users', and 'borrows' tables if they don't exist
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    conn = connect_db()
    cursor = conn.cursor()

    # Create 'books' table
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

    # Create 'users' table
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

    # Create 'borrows' table
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

# Import initial data from CSV files into respective tables
@app.route('/data', methods=['GET', 'POST'])
def add_data():
    conn = connect_db()
    cursor = conn.cursor()

    # Import data from 'books.csv'
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

    # Import data from 'users.csv'
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

    # Import data from 'borrow.csv'
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

# Route to manage books (GET for fetching all books, POST for adding a new book)
@app.route('/books', methods=['GET', 'POST'])
def manage_books():
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json()
        cursor.execute('''
            INSERT INTO books (isbn, isbn13, authors, publication_year, title, language_code, average_rating, ratings_count, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['isbn'], data['isbn13'], data['authors'], data['publication_year'],
            data['title'], data['language_code'], data['average_rating'], data['ratings_count'], data['image_url']
        ))
        conn.commit()
        book_id = cursor.lastrowid
        return jsonify({'message': 'Book added successfully!', 'book_id': book_id}), 201

    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return jsonify(books), 200

# Route to fetch details of a specific book by book_id
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
    book = cursor.fetchone()
    conn.close()

    if book is None:
        return jsonify({'error': 'Book not found.'}), 404
    
    return jsonify(book), 200

# Route to manage users (GET for fetching all users, POST for adding a new user)
@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json()
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, phone, address, membership_start_date, membership_end_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['first_name'], data['last_name'], data['email'], data['phone'], data['address'],
            data['membership_start_date'], data['membership_end_date']
        ))
        conn.commit()
        user_id = cursor.lastrowid
        return jsonify({'message': 'User added successfully!', 'user_id': user_id}), 201

    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return jsonify(users), 200

# Route to manage borrows (GET for fetching all borrows, POST for adding a new borrow)
@app.route('/borrows', methods=['GET', 'POST'])
def manage_borrows():
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json()
        cursor.execute('''
            INSERT INTO borrows (reader_id, book_id, borrow_date, return_date, is_returned)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['reader_id'], data['book_id'], data['borrow_date'], data['return_date'], data['is_returned']
        ))
        conn.commit()
        borrow_id = cursor.lastrowid
        return jsonify({'message': 'Borrow added successfully!', 'borrow_id': borrow_id}), 201

    cursor.execute('SELECT * FROM borrows')
    borrows = cursor.fetchall()
    conn.close()
    return jsonify(borrows), 200

# Route to delete a book by book_id
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Book deleted successfully!'}), 200

# Route to update a user by user_id
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

# Route to delete a user by user_id
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User deleted successfully!'}), 200

# Route to update a borrow by borrow_id
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

# Route to delete a borrow by borrow_id
@app.route('/borrows/<int:borrow_id>', methods=['DELETE'])
def delete_borrow(borrow_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM borrows WHERE borrow_id = ?', (borrow_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Borrow deleted successfully!'}), 200

# Route to search books by title, authors, isbn, or isbn13
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

# Route to update book details by book_id
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
