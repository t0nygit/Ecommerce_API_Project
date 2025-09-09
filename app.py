# app.py - Complete E-commerce API with All Endpoints

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Database configuration - Alternative approach
import urllib.parse

DB_USER = 'root'
DB_PASSWORD = urllib.parse.quote_plus('Q_u9whM_.Ynu9@FHVT2')  # URL encode the password
DB_HOST = 'localhost'
DB_NAME = 'ecommerce_api'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)

# ===== DATABASE MODELS =====

# Association table for many-to-many relationship between Orders and Products
order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class User(db.Model):
    """User model - can place multiple orders"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    
    # Relationship: One user can have many orders
    orders = db.relationship('Order', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.name}>'

class Product(db.Model):
    """Product model - can belong to multiple orders"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<Product {self.product_name}>'

class Order(db.Model):
    """Order model - belongs to one user, can contain multiple products"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Many-to-many relationship with products
    products = db.relationship('Product', secondary=order_product, lazy='subquery',
                             backref=db.backref('orders', lazy=True))
    
    def __repr__(self):
        return f'<Order {self.id}>'

# ===== MARSHMALLOW SCHEMAS =====

class UserSchema(ma.SQLAlchemyAutoSchema):
    """Schema for User serialization and validation"""
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

class ProductSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Product serialization and validation"""
    class Meta:
        model = Product
        load_instance = True
        sqla_session = db.session

class OrderSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Order serialization and validation"""
    class Meta:
        model = Order
        load_instance = True
        sqla_session = db.session
        include_fk = True  # Include foreign keys like user_id
    
    # Include nested user information
    user = ma.Nested(UserSchema, only=['id', 'name', 'email'])
    products = ma.Nested(ProductSchema, many=True)

# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# ===== USER ENDPOINTS =====

@app.route('/users', methods=['GET'])
def get_users():
    """GET /users: Retrieve all users"""
    try:
        users = User.query.all()
        return users_schema.jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """GET /users/<id>: Retrieve a user by ID"""
    try:
        user = User.query.get_or_404(id)
        return user_schema.jsonify(user), 200
    except Exception as e:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    """POST /users: Create a new user"""
    try:
        user_data = user_schema.load(request.json)
        db.session.add(user_data)
        db.session.commit()
        return user_schema.jsonify(user_data), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    """PUT /users/<id>: Update a user by ID"""
    try:
        user = User.query.get_or_404(id)
        user_data = user_schema.load(request.json, instance=user, partial=True)
        db.session.commit()
        return user_schema.jsonify(user_data), 200
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """DELETE /users/<id>: Delete a user by ID"""
    try:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'User {id} deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ===== PRODUCT ENDPOINTS =====

@app.route('/products', methods=['GET'])
def get_products():
    """GET /products: Retrieve all products"""
    try:
        products = Product.query.all()
        return products_schema.jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    """GET /products/<id>: Retrieve a product by ID"""
    try:
        product = Product.query.get_or_404(id)
        return product_schema.jsonify(product), 200
    except Exception as e:
        return jsonify({'error': 'Product not found'}), 404

@app.route('/products', methods=['POST'])
def create_product():
    """POST /products: Create a new product"""
    try:
        product_data = product_schema.load(request.json)
        db.session.add(product_data)
        db.session.commit()
        return product_schema.jsonify(product_data), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    """PUT /products/<id>: Update a product by ID"""
    try:
        product = Product.query.get_or_404(id)
        product_data = product_schema.load(request.json, instance=product, partial=True)
        db.session.commit()
        return product_schema.jsonify(product_data), 200
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    """DELETE /products/<id>: Delete a product by ID"""
    try:
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': f'Product {id} deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ===== ORDER ENDPOINTS =====

@app.route('/orders', methods=['POST'])
def create_order():
    """POST /orders: Create a new order"""
    try:
        # Validate that user exists
        user_id = request.json.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        order_data = order_schema.load(request.json)
        db.session.add(order_data)
        db.session.commit()
        return order_schema.jsonify(order_data), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['PUT'])
def add_product_to_order(order_id, product_id):
    """PUT /orders/<order_id>/add_product/<product_id>: Add a product to an order"""
    try:
        order = Order.query.get_or_404(order_id)
        product = Product.query.get_or_404(product_id)
        
        # Check if product is already in the order (prevent duplicates)
        if product in order.products:
            return jsonify({'message': 'Product already in order'}), 400
        
        order.products.append(product)
        db.session.commit()
        return order_schema.jsonify(order), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/orders/<int:order_id>/remove_product/<int:product_id>', methods=['DELETE'])
def remove_product_from_order(order_id, product_id):
    """DELETE /orders/<order_id>/remove_product/<product_id>: Remove a product from an order"""
    try:
        order = Order.query.get_or_404(order_id)
        product = Product.query.get_or_404(product_id)
        
        if product not in order.products:
            return jsonify({'error': 'Product not in order'}), 400
        
        order.products.remove(product)
        db.session.commit()
        return order_schema.jsonify(order), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    """GET /orders/user/<user_id>: Get all orders for a user"""
    try:
        user = User.query.get_or_404(user_id)
        orders = Order.query.filter_by(user_id=user_id).all()
        return orders_schema.jsonify(orders), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/orders/<int:order_id>/products', methods=['GET'])
def get_order_products(order_id):
    """GET /orders/<order_id>/products: Get all products for an order"""
    try:
        order = Order.query.get_or_404(order_id)
        return products_schema.jsonify(order.products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== TEST ROUTES =====

@app.route('/')
def home():
    return jsonify({
        'message': 'E-commerce API is running!',
        'endpoints': {
            'users': '/users',
            'products': '/products', 
            'create_tables': '/create-tables'
        }
    })

@app.route('/create-tables')
def create_tables():
    try:
        db.create_all()
        return jsonify({'message': 'Database tables created successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== ERROR HANDLERS =====

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create tables when app starts
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, port=8080)