from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    orders = db.relationship('Order', backref='user', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)
    wishlist = db.relationship('Wishlist', backref='user', lazy=True)
    chat_logs = db.relationship('ChatLog', backref='user', lazy=True)
    service_requests = db.relationship('ServiceRequest', backref='user', lazy=True)

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    supplier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    
    products = db.relationship('Product', backref='supplier', lazy=True)
    services = db.relationship('Service', backref='supplier', lazy=True)
    service_responses = db.relationship('ServiceResponse', backref='supplier', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id', ondelete="CASCADE"), nullable=False)
    
    orders = db.relationship('Order', backref='product', lazy=True)
    wishlist = db.relationship('Wishlist', backref='product', lazy=True)
    images = db.relationship('ProductImage', backref='product', lazy=True)

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id', ondelete="CASCADE"), nullable=False)
    
    payments = db.relationship('Payment', backref='order', lazy=True)
    tracking_updates = db.relationship('TrackingUpdate', backref='order', lazy=True)

class Payment(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete="CASCADE"), nullable=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id', ondelete="CASCADE"), nullable=True)

class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id', ondelete="CASCADE"), nullable=False)

class Service(db.Model):
    __tablename__ = 'services'
    service_id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id', ondelete="CASCADE"), nullable=False)

    bookings = db.relationship('Booking', backref='service', lazy=True)
    service_requests = db.relationship('ServiceRequest', backref='service', lazy=True)

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    service_request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id', ondelete="CASCADE"), nullable=False)

    service_responses = db.relationship('ServiceResponse', backref='service_request', lazy=True)

class ServiceResponse(db.Model):
    __tablename__ = 'service_responses'
    service_response_id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.service_request_id', ondelete="CASCADE"), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id', ondelete="CASCADE"), nullable=False)

class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    wishlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id', ondelete="CASCADE"), nullable=False)

class ProductImage(db.Model):
    __tablename__ = 'product_images'
    image_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id', ondelete="CASCADE"), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

class TrackingUpdate(db.Model):
    __tablename__ = 'tracking_updates'
    update_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete="CASCADE"), nullable=False)
    status = db.Column(db.String(255), nullable=False)

class ChatLog(db.Model):
    __tablename__ = 'chat_logs'
    chat_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    message = db.Column(db.Text, nullable=False)
