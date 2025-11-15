import os
from app import app

if __name__ == "__main__":
    # Ensure Flask knows the app entry point
    os.environ['FLASK_APP'] = 'app.py'
    
    # Run the application
    app.run(debug=True)