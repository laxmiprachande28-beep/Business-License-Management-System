# Business License Management System

A beginner-friendly web portal built using Python Flask, HTML, CSS, and MongoDB. The database follows the 8 entities in the ER diagram.

## Requirements
- Python 3
- MongoDB Community Server running locally OR a MongoDB Atlas connection string
- Visual Studio Code

## Setup in VS Code (Windows)

1. Open this project folder in VS Code.
2. Open Terminal: Terminal -> New Terminal.
3. Create a virtual environment:

   `py -m venv venv`

4. Activate it in PowerShell:

   `.\venv\Scripts\Activate.ps1`

   If PowerShell blocks activation, run this once in the terminal:

   `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

   Then activate again.

5. Install packages:

   `py -m pip install -r requirements.txt`

6. Copy `.env.example` and rename the copy to `.env`.
7. Make sure MongoDB is running. For local MongoDB, keep the URI:
   `mongodb://localhost:27017/`
8. Insert demo records:

   `py seed_data.py`

9. Start the website:

   `py app.py`

10. Open this address in your browser:

   `http://127.0.0.1:5000`

## Collections (8)
- applicants
- applications
- licenses
- officers
- documents
- payments
- businesses
- renewals

## Important
This is an educational prototype. It does not yet include real authentication, secure file upload, payment gateway integration, or production deployment.
