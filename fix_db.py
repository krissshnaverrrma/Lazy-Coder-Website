import os
from app import app, db 

# This script is for manually running db.create_all() or other setup commands
# in a local environment. 

with app.app_context():
    print("Attempting to create database tables defined in models...")
    try:
        db.create_all()
        print("Database tables created successfully (or already existed).")
    except Exception as e:
        print(f"ERROR: Could not create tables. Check your DB connection: {e}")