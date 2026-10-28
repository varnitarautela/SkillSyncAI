
import sqlite3

# Connect to the database
def connect_db():
    conn = sqlite3.connect("skillsync.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create the required database tables
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Student information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            skills TEXT NOT NULL
        )
    """)

    # Internship information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            skills_required TEXT NOT NULL,
            location TEXT
        )
    """)

    conn.commit()
    conn.close()

    print("Database tables created successfully!")


# Run the function
if __name__ == "__main__":
    create_tables()
