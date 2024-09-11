# E-commerce Backend - Python Flask & SQLite

This project consists of a backend system for an e-commerce platform, developed using Flask, SQLite, SQLAlchemy, and pytest. It includes features such as user management, product management, shopping cart handling, and order processing.

## Technologies used:
- **Python 3.8+**
- **Flask** as the web framework
- **SQLite** as the database
- **SQLAlchemy** as the ORM
- **Pytest** for unit testing
- **Git** for version control

## Table of Contents
- [Project Structure](#project-structure)
- [How to Run the Application](#how-to-run-the-application)
  - [Prerequisites](#prerequisites)
  - [Installing Dependencies](#installing-dependencies)
  - [Running the Application](#running-the-application)
  - [Usage](#usage)
  - [Features](#features)
  - [Main Endpoints](#main-endpoints)
- [Tests](#tests)
- [Implementation Approach and Trade-offs](#implementation-approach-and-trade-offs)
  - [Design Patterns Used](#design-patterns-used)
- [Learnings](#learnings)

## Project Structure
case_ecommerce_backend/
```bash│
├── app/
│   ├── __init__.py         # Initializes the Flask app
│   ├── models.py           # Database models
│   ├── services/           # Business logic
│   │   ├── account_service.py
│   │   ├── cart_controller.py
│   │   ├── order_controller.py
│   │   ├── product_controller.py  
│   │   └── user_controller.py  
│   └── controllers/        # Route controllers
│       ├── account_controller.py 
│       ├── cart_controller.py
│       ├── order_controller.py
│       ├── product_controller.py 
│       └── user_controller.py 
├── tests/                  # Unit tests
│   ├── test_cart_controller.py     
│   ├── test_product_controller.py
│   ├── test_user_controller.py    
├── app.py                  # Main Flask app entry point
├── requirements.txt        # Project dependencies
└── README.md               # Documentation
```

## How to run the application

### Prerequisites

Before starting, make sure you have Python 3.8 or later installed on your machine. You can check your Python version by running:

```bash
python --version
```

### Installing dependencies

Clone the repository and install the dependencies listed in the `requirements.txt` file
```bash
git clone https://github.com/Figueiredomth/case_ecommerce_backend.git
pip install -r requirements.txt
```

### Running the application
The project uses SQLite as the database. By default, the database configuration is already set up in the app.py file.

### Usage
To start the server locally, run the following command:
```bash
flask run
```
The server will be running at http://127.0.0.1:5000.

### Features
- Users: Register, login, logout
- Profile management: edit login and password or view the account information
- Products: Add, update, and delete products (admin only), List products for customers
- Cart: Add and clear items from the cart
- Orders: Create user orders

### Main Endpoints
http://127.0.0.1:5000/user/register: Register new users

*Request example*
```bash
POST http://127.0.0.1:5000/user/register
{
    "username": "user",
    "password": "password",
    "is_admin": true    #By default, this value is False, so if we want to create an admin user, we set this value as true
}
```
http://127.0.0.1:5000/user/login: User login

*Request example*
```bash
POST http://127.0.0.1:5000/user/login
{
    "username": "user",
    "password": "password"
}
```

http://127.0.0.1:5000/user/logout: User logout

*Request example*
```bash
GET http://127.0.0.1:5000/user/logout
```

http://127.0.0.1:5000/account: account management # Change username and/or password and get account information (`user_id` and `username`)

*Request example*
```bash
POST http://127.0.0.1:5000/account
{
    "new_username": "user",
    "new_password": "password"
}
```
or, if we want to get information about the account:
```bash
GET http://127.0.0.1:5000/account
```

http://127.0.0.1:5000/products/add: Add products in database (admin access required)

*Request example*
```bash
POST http://127.0.0.1:5000/products/add
{
    "name": "productexample",
    "description": "this product has this description",
    "price": 89.99,
    "stock": 50
}
```

http://127.0.0.1:5000/products/edit: Edit products information in database (admin access required)

*Request example*
```bash
PUT http://127.0.0.1:5000/products/edit
{
    "product_id": 1,
    "name": "productexample",
    "description": "this product has this description",
    "price": 89.99,
    "stock": 50
}
```

http://127.0.0.1:5000/products/delete: Delete products in database (admin access required)

*Request example*
```bash
DELETE http://127.0.0.1:5000/products/delete
{
    "product_id": 1
}
```

http://127.0.0.1:5000/products/list: List all products in database

*Request example*
```bash
GET http://127.0.0.1:5000/products/list
```

http://127.0.0.1:5000/products/details: Details all products in database

*Request example*
```bash
GET http://127.0.0.1:5000/products/details
```

http://127.0.0.1:5000/cart/add: Add products in the cart

*Request example*
```bash
POST http://127.0.0.1:5000/cart/add
{
  "product_id": 1,
  "quantity": 2
}
```

http://127.0.0.1:5000/cart/view: View the cart

*Request example*
```bash
GET http://127.0.0.1:5000/cart/view
```

http://127.0.0.1:5000/cart/clear: Clear the cart

*Request example*
```bash
DELETE http://127.0.0.1:5000/cart/clear
```

http://127.0.0.1:5000/order/checkout: Make a order based of what is in the cart

*Request example*
```bash
POST http://127.0.0.1:5000/order/checkout
```

### Environment Setup


### Tests

To run the unit tests, use pytest:
```bash
pytest
```
Tests are located in the `tests/` directory and cover the main functionalities, such as `user_controller`, `cart_controller`, and `product_controller`.


## Implementation Approach and Trade-offs
**Object-Oriented Design and Python Protocols**
The system was implemented using an **Object-Oriented Design (OOD)** approach, separating responsibilities into services (business logic) and controllers (route handling).

Initially, I began the project with a centralized approach, placing all resources and logic in a single file. While this setup allowed me to rapidly prototype features, it quickly became evident that this approach was neither efficient nor maintainable. The code became cluttered, making navigation and debugging increasingly difficult.

To address these issues, I refactored the codebase to adopt an **Object-Oriented Design (OOD)** approach. This involved separating responsibilities into distinct **services** and **controllers**. Services manage business logic, while controllers handle HTTP requests. This reorganization improved code clarity by isolating related functions and ensuring each component had a clear responsibility.

The benefits of this refactor included:

- **Clarity**: With related functions grouped into dedicated files, understanding the system's structure became easier.
- **Maintainability and Scalability**: The new structure allowed for easier integration of new features without adding complexity to existing functionality, making more scalable.
- **Testability**: Isolating business logic into services improved unit testing, as each component could be tested independently from request-handling logic.

Additionally, I adopted Python Protocols over traditional inheritance, aligning with the "Composition over Inheritance" principle. This approach allows for flexible behavior injection into classes (like `Product` and `Cart`), avoiding rigid hierarchical structures and enabling more adaptable design.

### Design Patterns Used

- **Service and Controller Layer Pattern**: This design pattern separates business logic from request handling, making the code more modular and easier to maintain. Each service interacts with the models and performs logic without directly managing HTTP requests.

### Trade-offs and Decisions

- **SQLite**: Chosen for its simplicity in local development and suitability for the project's requirements.
- **Error Handling**: Simple error messages were implemented for clarity.
- **Security**: Session-based authentication was used to handle user logins and interactions with accounts and products. This method ensures secure user identification while maintaining simplicity.

## Learnings

- **Flask and SQLAlchemy**: Enhanced understanding of RESTful API design and database management.
- **Error Management**: Improved skills in handling API responses and various error codes.
- **Unit Testing**: Gained experience in isolating and testing features independently.
- **Code Refactoring**: Recognized the importance of restructuring code mid-development. Transitioning from a monolithic design to a modular structure greatly improved code clarity and maintainability.

*Final Comment*: My expertise in backend development was limited before this project, with only basic implementations. However, this challenge was both demanding and rewarding. I significantly improved my skills in Python, database management, APIs, Git, and documentation.

