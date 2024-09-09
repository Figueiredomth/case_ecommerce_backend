# E-commerce Backend - Python Flask & SQLite

This project is a backend for an e-commerce system, developed in **Python Flask** with data persistence using **SQLite**. The backend includes functionalities such as **user registration and login**, **product management**, and **shopping cart**. In addition, there are **unit tests** to ensure code quality.

## Features

- User registration
- Authentication (login and logout)
- Product addition and listing (only admins can add, edit, and remove products)
- Shopping cart management
- Product stock control
- Data persistence using SQLite
- Unit testing with pytest

## Technologies

- **Python 3.8+**
- **Flask** as the web framework
- **SQLite** as the database
- **SQLAlchemy** as the ORM
- **Pytest** for unit testing
- **Git** for version control

## How to run the project

### Prerequisites

Before starting, make sure you have Python 3.8 or later installed on your machine. You can check your Python version by running:

```bash
python --version
```

### Installing dependencies

Clone the repository and install the dependencies listed in the `requirements.txt` file:

```bash
git clone https://github.com/Figueiredomth/case_commerce_backend.git
cd case_commerce_backend
pip install -r requirements.txt
```

### Running the application

After installing the dependencies, run the Flask application:
```bash
flask run
```

### Running the tests

To run the unit tests, use pytest:
```bash
pytest
```

### Project Structure
```bash
ecommerce-backend/
│
├── app.py
├── models.py
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_routes.py
├── requirements.txt
└── README.md
```

### Implemented Features
- User Registration: Users can sign up by providing a username and password (hashed).
- Authentication: The system supports login and logout, using token-based authentication.
- Product Management: Only admin users can add, edit, and remove products.
- ~~Shopping Cart: Users can add products to the cart and remove items, with stock control.~~ Under development
- Unit Testing: Tests are performed on login, registration routes, and product features.

