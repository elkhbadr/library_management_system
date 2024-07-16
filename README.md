# Library Management System

This project is a simple Library Management System implemented using Python (Flask) for the backend and HTML/CSS/JavaScript for the frontend.

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
- **Dependencies**: Flask, Flask-Cors (for handling CORS), SQLAlchemy (optional, for ORM)

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
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Flask server:

   ```bash
   python app.py
   ```

2. Open your web browser and go to `http://localhost:5000` to access the Library Management System.

### Usage

- **Adding a Book**: Click on "Add a Book" and fill in the details. Submit the form to add a new book.
- **Updating a Book**: Click on "Update a Book" to modify existing book details.
- **Adding a User**: Navigate to "Add a User" to create new library users.
- **Searching for Books**: Use the "Search Books" feature to find books by title, author, ISBN, or ISBN13.

### API Endpoints

- **POST `/books`**: Add a new book.
- **GET `/books`**: Retrieve all books.
- **GET `/books/<book_id>`**: Retrieve a specific book by ID.
- **POST `/books/<book_id>`**: Update an existing book.
- **DELETE `/books/<book_id>`**: Delete a book by ID.
- **GET `/users`**: Retrieve all users.
- **POST `/users`**: Add a new user.
- **GET `/search_books?q=<query>`**: Search for books by title, author, ISBN, or ISBN13.

### Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and create a pull request with your changes.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
