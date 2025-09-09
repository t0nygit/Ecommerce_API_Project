
# E-Commerce API Project

This is my Flask API project that creates an e-commerce system. The API can manage users, products, and orders using a MySQL database.

## What This Project 

- Create and manage users
- Create and manage products
- Create orders and add products to them
- Shows relationships between users, orders, and products
## Files In This Project

- app.py - Main Flask application with all the API endpoints
- E-commerce_API_Collection.json - Postman collection for testing the API
## Database Setup

I used MySQL Workbench to create a database called ecommerce_api. The app connects to MySQL running on my local machine.
## How to Run the Project

1. Install Requirements
```bash
pip install Flask Flask-SQLAlchemy Flask-Marshmallow marshmallow-sqlalchemy mysql-connector-python
```
2. Set Up Database
- Open MySQL Workbench
- Create a new database named ecommerce_api
- Update the password in app.py to match your MySQL password

3. Run the Application
```bash
python app.py
```
The API will run on http://127.0.0.1:8080

4. Create Database Tables
Visit http://127.0.0.1:8080/create-tables in your browser to create the tables.



## Testing with Postman

Import the E-commerce_API_Collection.json file into Postman to test all the API endpoints.


## API Endpoints

Users
- GET /users - Get all users
- POST /users - Create a new user
- GET /users/<id> - Get user by ID
- PUT /users/<id> - Update user
- DELETE /users/<id> - Delete user

Products
- GET /products - Get all products
- POST /products - Create a new product
- GET /products/<id> - Get product by ID
- PUT /products/<id> - Update product
- DELETE /products/<id> - Delete product

Orders
- POST /orders - Create a new order
- PUT /orders/<order_id>/add_product/<product_id> - Add product to order
- DELETE /orders/<order_id>/remove_product/<product_id> - Remove product from order
- GET /orders/user/<user_id> - Get all orders for a user
- GET /orders/<order_id>/products - Get all products in an order
## Database Models

- User: Has name, address, email
- Product: Has product name and price
- Order: Belongs to a user and can have many products
- Order_Product: Association table linking orders and products
## What I Learned

- How to create a Flask API with database connections
- Setting up relationships between database tables
- Using Marshmallow for data validation and serialization
- Testing APIs with Postman
- Working with MySQL and SQLAlchemy

## 🚀 About Me
I'm a beginner software engineer in a coding bootcamp at Coding Temple

## 🔗 Links
https://github.com/t0nygit



