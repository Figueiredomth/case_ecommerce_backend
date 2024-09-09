# E-commerce Backend System

## Overview
This project is a robust backend for an e-commerce application, designed to handle core functionalities such as user registration, product management, shopping cart functionality, and order processing. Built using Python, Flask, SQLAlchemy, and SQLite, this application provides a solid foundation for building a comprehensive e-commerce platform.

## Key Features:
User Management:
Secure user registration and login with password hashing.
Profile management for personalized user experiences.

Product Catalog:
Comprehensive product management for admins, including adding, editing, and removing products.
Detailed product information and categorization.

Shopping Cart:
Dynamic shopping cart functionality, allowing users to add, remove, and update items.
Ability to save carts for later and retrieve order history.

Checkout Process:
Secure checkout process with various payment gateway integrations (optional).
Order confirmation and email notifications.

## Technical Stack:
Python: A versatile programming language for web development.
Flask: A lightweight and flexible Python web framework.
SQLAlchemy: An Object-Relational Mapper (ORM) that simplifies database interactions.
SQLite: An embedded SQL database for storing application data.


### Project Structure
- models.py: Defines the data models.
- app.py: Contains application routes and logic

## Development Stages
### 1. Initial Setup
Set up the Flask environment and configured SQLAlchemy.
Decided to use SQLAlchemy because it offers a robust and efficient Object-Relational Mapping (ORM) system that simplifies interactions with the SQLite database. By using SQLAlchemy, I can easily map Python objects to database tables, which makes managing user, product, and order data more intuitive.
Initialized the database with users, products, and orders tables
I created the database in the firsts stages to have an idea to what and how build the functions in the main application.


### 2. Data Models (models.py)
User: Models a user with attributes id, username, password, and is_admin.
Decisions:
Added is_admin column to determine if a user has administrative privileges.
Usernames and passwords must meet minimum requirements.

Product: Models a product with attributes id, name, description, price, and stock.
Decisions:
Validated that price and stock cannot be negative and stock have to be an integer number.
Products cannot have negative prices or stock.

Order: Models an order with attributes id, user_id, order_date, and total.
Related the order to the user who placed it.

### 3. Application Logic (app.py)
User Registration (/register):
Implemented to create new users with input validation and the option to set an admin status.

User Login (/login):
Decisions:
Checked credentials and managed user session.
Allow same request to login as a different user to simulate an environment that the same person can login in a different account.

Logout (/logout):
End the user's session.

Account Management (/account):
Allowed users to update their username and password.

Add Product (/products):
Decisions:
Restricted access to administrators and validated product data, datatype, etc


### Next Steps
Add functionalities for editing and removing products.
Implement unit tests to ensure system integrity as i add new features.
