# Lazy Coder Blog 💻

This is a full-featured blog application built with Flask, designed for easy content creation, management, and deployment. The application supports user authentication, image uploading, and a cloud-hosted relational database.

**Live Demo:** [**https://lazy-coder-website.onrender.com/**](https://lazy-coder-website.onrender.com/)

## ✨ Features

* **User Authentication:** Secure user registration, login, and logout.
* **Account Recovery:** "Forgot Password" system using a secure, question-based method (no email required).
* **Database Persistence:** Configured for deployment using a persistent **PostgreSQL** database (via `DATABASE_URL`) with a fallback to local SQLite.
* **CRUD Operations:** Full Create, Read, Update, and Delete (CRUD) capability for blog posts.
* **Image Management:**
    * Profile picture uploads and dynamic resizing using Pillow.
    * Blog post header image uploads with dedicated storage and cleanup logic.
    * Associated images are deleted from storage when a post or account is removed.
* **Full-Text Search:** A search bar to find posts by keywords in the title or content.

## 🛠️ Tech Stack

* **Backend:** [**Flask**](https://flask.palletsprojects.com/) & [**Gunicorn**](https://gunicorn.org/)
* **Database:** [**PostgreSQL**](https://www.postgresql.org/) (Production) / [**SQLite**](https://www.sqlite.org/index.html) (Local)
* **ORM:** [**SQLAlchemy**](https://www.sqlalchemy.org/)
* **Image Handling:** [**Pillow**](https://python-pillow.org/)
* **PostgreSQL Driver:** [**psycopg2-binary**](https://pypi.org/project/psycopg2-binary/)

## 🚀 Deployment

This project is structured for easy deployment to platforms like Render.

### Local Setup

1.  Clone the repository:
    ```bash
    git clone [https://github.com/krisshnaverrrma/Lazy-Coder-Website.git](https://github.com/krisshnaverrrma/Lazy-Coder-Website.git)
    cd Lazy-Coder-Website
    ```
2.  Create and activate a virtual environment:
    ```bash
    # On Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Set up environment variables (create a `.env` file):
    ```.env
    SECRET_KEY="YOUR_VERY_LONG_SECRET_KEY"
    # The DATABASE_URL is optional, it will default to SQLite
    # DATABASE_URL="sqlite:///lazy_blog.db"
    ```
5.  Run the application:
    ```bash
    flask run
    ```
    Open `http://127.0.0.1:5000` in your browser.

### Cloud Deployment (Render)

1.  **Set Environment Variables** in the Render dashboard:
    * `SECRET_KEY`: A new, strong random string.
    * `DATABASE_URL`: The **Internal Connection String** from your Render PostgreSQL database.
2.  **Set Commands** in the Render dashboard:
    * **Build Command:** `pip install -r requirements.txt`
    * **Start Command:** `gunicorn app:app`

---

## 🐍 `requirements.txt` (Final Dependencies)

This file lists all the libraries necessary for both development and production.

```text:requirements.txt
Flask
Flask-SQLAlchemy
Flask-Login
python-dotenv
itsdangerous
Pillow
gunicorn
psycopg2-binary