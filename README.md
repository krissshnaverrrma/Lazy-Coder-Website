# Lazy Coder Blog 💻

This is a full-featured blog application built with Flask, designed for easy content creation, management, and deployment. The application supports user authentication, image uploading, and a cloud-hosted relational database.

## ✨ Features

* **User Authentication:** Secure user registration, login, logout, and password reset functionality using Flask-Login and Flask-Mail.
* **Database Persistence:** Configured for deployment using a persistent **PostgreSQL** database (via `DATABASE_URL` environment variable) with a fallback to local SQLite.
* **CRUD Operations:** Full Create, Read, Update, and Delete (CRUD) capability for blog posts.
* **Image Management:**
    * Profile picture uploads and dynamic resizing using Pillow.
    * Blog post header image uploads with dedicated storage and cleanup logic.
    * Associated images are deleted from storage when a post or account is removed.
* **Responsive UI:** Clean, standard CSS design optimized for readability and card layout.

## 🚀 Deployment

This project is structured for easy deployment to platforms like Render or Heroku.

### Prerequisites

1.  **Python Environment:** Python 3.9+ and a virtual environment (`venv`).
2.  **External Database:** A persistent PostgreSQL database (required for cloud hosting).
3.  **App Password:** An App Password must be generated if using Gmail for `FLASK_MAIL_PASSWORD`.

### Local Setup

1.  Clone the repository:
    ```bash
    git clone [YOUR_REPO_URL]
    cd Lazy-Coder-Website
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Set up environment variables (create a `.env` file):
    ```
    SECRET_KEY="YOUR_VERY_LONG_SECRET_KEY"
    FLASK_MAIL_USERNAME="your.email@gmail.com"
    FLASK_MAIL_PASSWORD="your_app_password"
    # Optional: DATABASE_URL for local testing with external DB
    ```
5.  Initialize the database tables (this must be run once):
    ```bash
    # The automatic db.create_all() will run on first execution
    python app.py
    ```

### Cloud Deployment (Render/Heroku/Vercel)

The application is configured to run using Gunicorn and read the database connection string from the hosting environment.

1.  **Set Environment Variables:** Configure the following four required variables in the host dashboard:
    * `SECRET_KEY`
    * `FLASK_MAIL_USERNAME`
    * `FLASK_MAIL_PASSWORD`
    * **`DATABASE_URL`** (The full PostgreSQL connection string).
2.  **Procfile:** The host will execute the start command defined in the `Procfile`: `web: gunicorn app:app`

---

## 2. 🐍 `requirements.txt` (Final Dependencies)

This file lists all the libraries necessary for both development and production.

```text:requirements.txt
Flask
Flask-SQLAlchemy
Flask-Login
python-dotenv
Flask-Mail
itsdangerous
Pillow
gunicorn
psycopg2-binary  # PostgreSQL driver
```eof