from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.extensions import db
from app.models import Product, Supplier

# Define the supplier blueprint
supplier_bp = Blueprint("supplier", __name__)

# Supplier dashboard to view all products
@supplier_bp.route('/dashboard')
def dashboard():
    products = Product.query.all()
    return render_template('supplier/dashboard.html', products=products)

# Add a new product
@supplier_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form.get('description', '')
        stock = int(request.form.get('stock', 0))
        accreditation = request.form.get('accreditation', '')

        # Placeholder for logged-in supplier
        supplier_id = 1  

        new_product = Product(
            name=name, 
            price=price, 
            description=description, 
            stock=stock, 
            accreditation=accreditation, 
            supplier_id=supplier_id
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('supplier.dashboard'))

    return render_template('supplier/add_product.html')

# View and update product details
@supplier_bp.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_details(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.description = request.form.get('description', '')
        product.stock = int(request.form.get('stock', 0))
        product.accreditation = request.form.get('accreditation', '')
        db.session.commit()
        flash('Product details updated successfully!', 'success')
        return redirect(url_for('supplier.dashboard'))

    return render_template('supplier/product_details.html', product=product)

# Edit an existing product (minimal fields)
@supplier_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('supplier.dashboard'))

    return render_template('supplier/edit_product.html', product=product)

# Delete a product
@supplier_bp.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('supplier.dashboard'))
