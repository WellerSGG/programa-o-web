from flask import request, jsonify, Blueprint
from app.models import db, User, Product, Order

auth_bp = Blueprint('auth', __name__)
user_bp = Blueprint('user', __name__)
product_bp = Blueprint('product', __name__)
order_bp = Blueprint('order', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@product_bp.route('/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'POST':
        data = request.get_json()
        product = Product(name=data['name'], price=data['price'], description=data['description'])
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product created successfully'}), 201
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price, 'description': p.description} for p in products])

@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user = User.query.get(data['user_id'])
    products = Product.query.filter(Product.id.in_(data['product_ids'])).all()
    order = Order(user_id=user.id, total=sum([p.price for p in products]), products=products)
    db.session.add(order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201
