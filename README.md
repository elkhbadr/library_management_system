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

- **POST `/books`**: Add a new book.
- **GET `/books`**: Retrieve all books.
- **GET `/books/<book_id>`**: Retrieve a specific book by ID.
- **POST `/books/<book_id>`**: Update an existing book.
- **DELETE `/books/<book_id>`**: Delete a book by ID.
- **GET `/users`**: Retrieve all users.
- **POST `/users`**: Add a new user.
- **POST `/search_books?q=<query>`**: Search for books by title, author, ISBN, or ISBN13.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
