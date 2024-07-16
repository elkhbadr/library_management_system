# Library Management System

This project is a simple Library Management System implemented using Python (Flask) for the backend and HTML/CSS/JavaScript for the frontend, using SQLite for the database.

## Features

- **Add a Book**: Allows users to add new books to the library.
- **Update a Book**: Enables editing existing book details.
- **Add a User**: Allows librarians to add new library users.
- **Add a Borrow**: Enables tracking of book borrowings.
- **Search Books**: Provides search functionality to find books by title, author, ISBN, or ISBN13.

## Technologies Used

- **Backend**: Python, Flask, SQLite (for local database)
- **Frontend**: HTML, CSS (Bootstrap), JavaScript (jQuery)
- **Database**: SQLite (can be easily swapped with other SQL databases like MySQL, PostgreSQL)
- **Dependencies**: Flask, Flask-Cors (for handling CORS)

## Getting Started

### Prerequisites

- Python 3.x installed on your system.
- Flask and necessary libraries installed (`pip install flask flask-cors`).

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
   ```

2. Install dependencies:

   ```bash
   pip install -r flask flask-cors
   ```

### Running the Application

1. Start the Flask server:

   ```bash
   python app.py
   ```

2. Setup Virtual Environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Intialize the database:

   ```bash
   curl -X GET http://localhost:5000/setup
   ```	

4. Import data(optional):

   ```bash
   curl -X GET http://localhost:5000/data
   ```	
The database used in this project is based on the [Goodreads Books Dataset](https://www.kaggle.com/zygmunt/goodbooks-10k), provided in the `data` directory. You can use this pre-provided database or replace it with your own dataset.


5. Open your web browser and go to `http://localhost:5000` to access the Library Management System.

### Usage

- **Adding a Book**: Click on "Add a Book" and fill in the details. Submit the form to add a new book.
- **Updating a Book**: Click on "Update a Book" to modify existing book details.
- **Adding a User**: Navigate to "Add a User" to create new library users.
- **Adding a Borrow**: Navigate to "Add a Borrow" to create new borrows.
- **Searching for Books**: Use the "Search Books" feature to find books by title, author, ISBN, or ISBN13.

### API Endpoints

#### Books

- **GET /books**  
  Retrieves a list of all books in the library.

- **POST /books**  
  Adds a new book to the library database.

- **GET /books/{book_id}**  
  Retrieves details of a specific book by `book_id`.

- **DELETE /books/{book_id}**  
  Deletes a book from the library by `book_id`.

- **POST /update_book**  
  Updates details of a book identified by `book_id`.

#### Users

- **GET /users**  
  Retrieves a list of all users in the library system.

- **POST /users**  
  Adds a new user to the library system.

- **PUT /users/{user_id}**  
  Updates details of a user identified by `user_id`.

- **DELETE /users/{user_id}**  
  Deletes a user from the library system by `user_id`.

#### Borrows

- **GET /borrows**  
  Retrieves a list of all borrow records in the library.

- **POST /borrows**  
  Adds a new borrow record for a user borrowing a book.

- **PUT /borrows/{borrow_id}**  
  Updates details of a borrow record identified by `borrow_id`.

- **DELETE /borrows/{borrow_id}**  
  Deletes a borrow record from the library by `borrow_id`.

#### Setup and Data Import

- **POST /setup**  
  Initializes the database by creating necessary tables (`books`, `users`, `borrows`).

- **POST /data**  
  Imports initial data from CSV files (`books.csv`, `users.csv`, `borrow.csv`) into the database tables.

#### Additional Functionality

- **POST /search_books**  
  Searches for books by title, author, ISBN, or ISBN13.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
