import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define Book class
class Book:
    # Define reading status constants
    STATUS_UNREAD = "unread"
    STATUS_IN_PROGRESS = "in-progress"
    STATUS_COMPLETED = "completed"
    
    def __init__(self, title, author, publication_year, genre, read_status=STATUS_UNREAD):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.genre = genre
        self.read_status = read_status
    
    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'publication_year': self.publication_year,
            'genre': self.genre,
            'read_status': self.read_status
        }

    def get_status_display(self):
        if self.read_status == self.STATUS_UNREAD:
            return "Unread"
        elif self.read_status == self.STATUS_IN_PROGRESS:
            return "In Progress"
        elif self.read_status == self.STATUS_COMPLETED:
            return "Completed"
        return self.read_status  # Fallback

# Functions for file operations
def save_books(books):
    try:
        with open('library.json', 'w') as f:
            json.dump([book.to_dict() for book in books], f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving library: {str(e)}")
        return False

def load_books():
    if not os.path.exists('library.json'):
        return []
    
    try:
        with open('library.json', 'r') as f:
            data = json.load(f)
            books = []
            for book in data:
                # Handle legacy boolean read_status
                if isinstance(book['read_status'], bool):
                    read_status = Book.STATUS_COMPLETED if book['read_status'] else Book.STATUS_UNREAD
                else:
                    read_status = book['read_status']
                
                books.append(Book(
                    book['title'],
                    book['author'],
                    book['publication_year'],
                    book['genre'],
                    read_status
                ))
            return books
    except json.JSONDecodeError:
        st.warning("Error reading library file. Starting with empty library.")
        return []
    except Exception as e:
        st.error(f"Error loading library: {str(e)}")
        return []

# Initialize session state
if 'books' not in st.session_state:
    st.session_state.books = load_books()

if 'page' not in st.session_state:
    st.session_state.page = "Add Book"

# Functions for book operations
def add_book(title, author, year, genre, read_status):
    # Convert boolean to string status if needed
    if isinstance(read_status, bool):
        read_status = Book.STATUS_COMPLETED if read_status else Book.STATUS_UNREAD
    
    book = Book(title, author, year, genre, read_status)
    st.session_state.books.append(book)
    return save_books(st.session_state.books)

def remove_book(title):
    original_count = len(st.session_state.books)
    st.session_state.books = [book for book in st.session_state.books 
                             if book.title.lower() != title.lower()]
    if len(st.session_state.books) < original_count:
        return save_books(st.session_state.books)
    return False

def update_book_status(title, new_status):
    for book in st.session_state.books:
        if book.title.lower() == title.lower():
            book.read_status = new_status
            return save_books(st.session_state.books)
    return False

def search_books(search_term):
    search_term = search_term.lower()
    return [book for book in st.session_state.books 
            if search_term in book.title.lower() or search_term in book.author.lower()]

def calculate_stats():
    total_books = len(st.session_state.books)
    completed_books = sum(1 for book in st.session_state.books if book.read_status == Book.STATUS_COMPLETED)
    in_progress_books = sum(1 for book in st.session_state.books if book.read_status == Book.STATUS_IN_PROGRESS)
    unread_books = total_books - completed_books - in_progress_books
    
    percentage_read = (completed_books / total_books * 100) if total_books > 0 else 0
    percentage_in_progress = (in_progress_books / total_books * 100) if total_books > 0 else 0
    
    return {
        'total_books': total_books,
        'completed_books': completed_books,
        'in_progress_books': in_progress_books,
        'unread_books': unread_books,
        'percentage_read': percentage_read,
        'percentage_in_progress': percentage_in_progress
    }

def change_page(page_name):
    st.session_state.page = page_name

# Sidebar navigation
with st.sidebar:
    st.title("📚 Library Manager")
    st.markdown("---")
    
    if st.button("📕 Add Book", use_container_width=True):
        change_page("Add Book")
    
    if st.button("📚 View Library", use_container_width=True):
        change_page("View Library")
    
    if st.button("🔍 Search", use_container_width=True):
        change_page("Search")
    
    if st.button("📊 Statistics", use_container_width=True):
        change_page("Statistics")
    
    st.markdown("---")
    st.caption("Personal Library Manager v1.0")

# Main content
st.title("📚 Personal Library Manager")

# Add Book page
if st.session_state.page == "Add Book":
    st.header("Add New Book")
    
    with st.form(key="add_book_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title")
            author = st.text_input("Author")
            year = st.number_input("Publication Year", 
                                  min_value=1800, 
                                  max_value=datetime.now().year,
                                  value=2000)
        
        with col2:
            genre = st.text_input("Genre")
            read_status = st.selectbox(
                "Reading Status",
                options=[Book.STATUS_UNREAD, Book.STATUS_IN_PROGRESS, Book.STATUS_COMPLETED],
                format_func=lambda x: x.capitalize().replace('-', ' ')
            )
        
        submitted = st.form_submit_button("Add Book")
        
        if submitted:
            if not title or not author or not genre:
                st.error("Please fill in all required fields (Title, Author, and Genre).")
            else:
                if add_book(title, author, year, genre, read_status):
                    st.success(f"Successfully added '{title}' to your library!")
                else:
                    st.error("Failed to add the book. Please try again.")

# View Library page
elif st.session_state.page == "View Library":
    st.header("Your Library")
    
    if not st.session_state.books:
        st.info("Your library is empty. Add some books to get started!")
    else:
        # Function to handle delete button click
        def delete_callback(title):
            if remove_book(title):
                st.success(f"Successfully removed '{title}' from your library!")
                st.rerun()
            else:
                st.error(f"Failed to remove '{title}'")
        
        # Function to handle status update
        def update_status_callback(title, new_status):
            if update_book_status(title, new_status):
                st.success(f"Updated '{title}' status to {new_status.capitalize().replace('-', ' ')}!")
                st.rerun()
            else:
                st.error(f"Failed to update status for '{title}'")
        
        # Display books in a clean format
        for i, book in enumerate(st.session_state.books):
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(book.title)
                    st.write(f"**Author:** {book.author}")
                    st.write(f"**Year:** {book.publication_year} | **Genre:** {book.genre} | **Status:** {book.get_status_display()}")
                
                with col2:
                    # Status update dropdown
                    new_status = st.selectbox(
                        "Update Status",
                        options=[Book.STATUS_UNREAD, Book.STATUS_IN_PROGRESS, Book.STATUS_COMPLETED],
                        index=[Book.STATUS_UNREAD, Book.STATUS_IN_PROGRESS, Book.STATUS_COMPLETED].index(book.read_status),
                        format_func=lambda x: x.capitalize().replace('-', ' '),
                        key=f"status_{i}"
                    )
                    
                    col2a, col2b = st.columns(2)
                    with col2a:
                        if st.button("Update", key=f"update_{i}", use_container_width=True):
                            if new_status != book.read_status:
                                update_status_callback(book.title, new_status)
                    
                    with col2b:
                        if st.button("Delete", key=f"delete_{i}", use_container_width=True):
                            delete_callback(book.title)
                
                st.markdown("---")

# Search page
elif st.session_state.page == "Search":
    st.header("Search Books")
    
    search_term = st.text_input("Search by title or author")
    
    if search_term:
        results = search_books(search_term)
        
        if not results:
            st.info(f"No books found matching '{search_term}'")
        else:
            st.write(f"Found {len(results)} matching books:")
            
            for book in results:
                with st.container():
                    st.subheader(book.title)
                    st.write(f"**Author:** {book.author}")
                    st.write(f"**Year:** {book.publication_year} | **Genre:** {book.genre} | **Status:** {book.get_status_display()}")
                    st.markdown("---")

# Statistics page
elif st.session_state.page == "Statistics":
    st.header("Library Statistics")
    
    stats = calculate_stats()
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Books", stats['total_books'])
    with col2:
        st.metric("Completed", stats['completed_books'])
    with col3:
        st.metric("In Progress", stats['in_progress_books'])
    with col4:
        st.metric("Unread", stats['unread_books'])
    
    # Create visualization if there are books
    if stats['total_books'] > 0:
        st.subheader("Reading Progress")
        
        fig = go.Figure(data=[go.Pie(
            labels=['Completed', 'In Progress', 'Unread'],
            values=[stats['completed_books'], stats['in_progress_books'], stats['unread_books']],
            hole=.4,
            marker_colors=['#2ca02c', '#ff7f0e', '#1f77b4']  # Green, Orange, Blue
        )])
        
        fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show genre distribution
        if stats['total_books'] > 1:
            genre_counts = {}
            for book in st.session_state.books:
                genre_counts[book.genre] = genre_counts.get(book.genre, 0) + 1
            
            st.subheader("Genre Distribution")
            
            genre_fig = go.Figure(data=[go.Bar(
                x=list(genre_counts.keys()),
                y=list(genre_counts.values())
            )])
            
            genre_fig.update_layout(
                xaxis_title="Genre",
                yaxis_title="Number of Books",
                margin=dict(t=20, b=20, l=20, r=20),
                height=400
            )
            
            st.plotly_chart(genre_fig, use_container_width=True) 