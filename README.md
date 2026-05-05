# Final-Project-ITC-345-Introduction-to-Python
# 📚 Library Management System

## Overview
This is a Flask-based Library Management System built with Python and SQLite. It allows administrators to manage books and users, track borrowing history, and generate reports. The project includes a simple web interface and test suite.

---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/hamidasana-coder/Final-Project-ITC-345-Introduction-to-Python.git
   cd Final-Project-ITC-345-Introduction-to-Python/librarymanagment
   
## 📦 Installation Dependencies

Install all required packages using:

```bash
pip install -r requirements.txt

```
## nitialize the database:
flask shell
>>> from models import db
>>> db.create_all()

## Run the application:
flask run
The app will be available at:
http://127.0.0.1:5000

## **Documentation**
Additional documentation (API endpoints and database schema) is available in:
python final project documentation/

## 👩‍💻 **Contributors**
- Hamida Sana — Repository setup, README documentation, Testing, Additional python code 
- Husna Sadat — frontend, API, hub, database schema, models
- Najma Yousofi — APi, Hub, models

##✅ **Deliverables Checklist**

[x] GitHub repository with clear commit history

[x] README.md with setup and usage instructions

[x] Documentation (API + schema)

[x] Flask source code organized into modules

[x] Normalized SQLite database schema


## ✅ Testing Report
We included both **unit tests** and **integration tests** to ensure the application functions correctly.
- **Unit Tests**: Verify individual functions and models (e.g., book creation, user management).
- **Integration Tests**: Verify system flows (e.g., borrowing books, generating reports).

### Test Execution
All tests were run inside the virtual environment using:

```bash
python -m pytest

(venv) PS C:\Users\salim\ibrary-management-system\librarymanagment> python -m pytest
============================================ test session starts ============================================
platform win32 -- Python 3.14.2, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\salim\ibrary-management-system\librarymanagment
collected 15 items

tests\test_books.py ....                                                                               [ 26%]
tests\test_borrow.py .                                                                                 [ 33%]
tests\test_report.py ..                                                                                [ 46%]
tests\test_users.py ........                                                                           [100%]

============================================ 15 passed in 1.01s =============================================







  
