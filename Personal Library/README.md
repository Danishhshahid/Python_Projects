# Personal Library Manager

A command-line application for managing your personal book collection. This program allows you to add, remove, search, and track your books, including their read status.

## Features

- Add new books with details (title, author, publication year, genre, read status)
- Remove books from your collection
- Search for books by title or author
- Display all books in a formatted table
- View library statistics (total books, read/unread counts, percentage read)
- User-friendly menu interface

## Requirements

- Python 3.6 or higher

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Run the program using Python:
   ```
   python library_manager.py
   ```

## Usage

1. Launch the program
2. Use the menu options (1-6) to:
   - Add new books
   - Remove existing books
   - Search your collection
   - View all books
   - Check library statistics
   - Exit the program

3. Follow the prompts to enter book details when adding new books
4. Use the search function to find books by title or author name

## Book Details

Each book in the library contains the following information:
- Title
- Author
- Publication Year (between 1800 and 2024)
- Genre
- Read Status (Read/Unread)

## Example Usage

```
=== Personal Library Manager ===
1. Add a book
2. Remove a book
3. Search for a book
4. Display all books
5. Display statistics
6. Exit

Enter your choice (1-6): 1

=== Add a New Book ===
Enter book title: The Great Gatsby
Enter author name: F. Scott Fitzgerald
Enter publication year: 1925
Enter genre: Classic
Have you read this book? (y/n): y

Successfully added 'The Great Gatsby' to your library! 