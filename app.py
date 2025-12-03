import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from decimal import Decimal
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'emunah-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///emunah.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='SELLER')
    phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    cpf_cnpj = db.Column(db.String(20))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    contact_name = db.Column(db.String(255))
    cnpj = db.Column(db.String(20))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    production_time_days = db.Column(db.Integer, default=7)
    rating = db.Column(db.Numeric(2, 1), default=0)
    payment_method = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    fabric = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    sizes = db.Column(db.JSON, nullable=False)
    base_price = db.Column(db.Numeric(10, 2), default=0)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Print(db.Model):
    __tablename__ = 'prints'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    file_url = db.Column(db.String(500))
    colors = db.Column(db.JSON, nullable=False)
    positions = db.Column(db.JSON, nullable=False)
    technique = db.Column(db.String(50), default='silk')
    dimensions = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    print_id = db.Column(db.Integer, db.ForeignKey('prints.id'))
    items = db.Column(db.JSON, nullable=False)
    status = db.Column(db.String(50), default='pending')
    total_quantity = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Numeric(10, 2))
    total_price = db.Column(db.Numeric(10, 2))
    delivery_days = db.Column(db.Integer)
    supplier_response = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    responded_at = db.Column(db.DateTime)

    client = db.relationship('Client', backref='quotes')
    seller = db.relationship('User', backref='quotes')
    supplier = db.relationship('Supplier', backref='quotes')

class Budget(db.Model):
    __tablename__ = 'budgets'
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    budget_number = db.Column(db.String(50), unique=True, nullable=False)
    total_value = db.Column(db.Numeric(10, 2), nullable=False)
    down_payment_percent = db.Column(db.Integer, default=50)
    down_payment_value = db.Column(db.Numeric(10, 2), nullable=False)
    pix_key = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='draft')
    valid_until = db.Column(db.DateTime, nullable=False)
    pdf_url = db.Column(db.String(500))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime)
    approved_at = db.Column(db.DateTime)

    quote = db.relationship('Quote', backref='budgets')
    client = db.relationship('Client', backref='budgets')

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(50), default='approved')
    production_step = db.Column(db.String(50), default='cutting')
    progress = db.Column(db.Integer, default=0)
    total_value = db.Column(db.Numeric(10, 2), nullable=False)
    delivery_date = db.Column(db.DateTime)
    tracking_code = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    delivered_at = db.Column(db.DateTime)

    budget = db.relationship('Budget', backref='orders')
    client = db.relationship('Client', backref='orders')
    supplier = db.relationship('Supplier', backref='orders')

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), default='pending')
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    order = db.relationship('Order', backref='transactions')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_dashboard_metrics():
    total_revenue = db.session.query(db.func.coalesce(db.func.sum(Order.total_value), 0)).filter(Order.status == 'delivered').scalar()
    completed_orders = Order.query.filter_by(status='delivered').count()
    pending_budgets = Budget.query.filter_by(status='sent').count()
    avg_ticket = db.session.query(db.func.coalesce(db.func.avg(Order.total_value), 0)).filter(Order.status == 'delivered').scalar()
    return {
        'total_revenue': float(total_revenue) if total_revenue else 0,
        'completed_orders': completed_orders,
        'pending_budgets': pending_budgets,
        'average_ticket': float(avg_ticket) if avg_ticket else 0
    }

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        flash('Email ou senha inválidos.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    metrics = get_dashboard_metrics()
    orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    budgets = Budget.query.order_by(Budget.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', metrics=metrics, orders=orders, budgets=budgets)

@app.route('/suppliers')
@login_required
def suppliers():
    suppliers_list = Supplier.query.order_by(Supplier.created_at.desc()).all()
    return render_template('suppliers.html', suppliers=suppliers_list)

@app.route('/suppliers/new', methods=['GET', 'POST'])
@login_required
def new_supplier():
    if request.method == 'POST':
        supplier = Supplier(
            name=request.form.get('name'),
            contact_name=request.form.get('contact_name'),
            cnpj=request.form.get('cnpj'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            address=request.form.get('address'),
            production_time_days=int(request.form.get('production_time_days', 7)),
            rating=float(request.form.get('rating', 0)),
            payment_method=request.form.get('payment_method'),
            notes=request.form.get('notes')
        )
        db.session.add(supplier)
        db.session.commit()
        flash('Fornecedor criado com sucesso!', 'success')
        return redirect(url_for('suppliers'))
    return render_template('supplier_form.html', supplier=None)

@app.route('/suppliers/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    if request.method == 'POST':
        supplier.name = request.form.get('name')
        supplier.contact_name = request.form.get('contact_name')
        supplier.cnpj = request.form.get('cnpj')
        supplier.email = request.form.get('email')
        supplier.phone = request.form.get('phone')
        supplier.address = request.form.get('address')
        supplier.production_time_days = int(request.form.get('production_time_days', 7))
        supplier.rating = float(request.form.get('rating', 0))
        supplier.payment_method = request.form.get('payment_method')
        supplier.notes = request.form.get('notes')
        db.session.commit()
        flash('Fornecedor atualizado com sucesso!', 'success')
        return redirect(url_for('suppliers'))
    return render_template('supplier_form.html', supplier=supplier)

@app.route('/suppliers/<int:id>/delete', methods=['POST'])
@login_required
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    flash('Fornecedor excluído com sucesso!', 'success')
    return redirect(url_for('suppliers'))

@app.route('/prints')
@login_required
def prints():
    prints_list = Print.query.order_by(Print.created_at.desc()).all()
    return render_template('prints.html', prints=prints_list)

@app.route('/prints/new', methods=['GET', 'POST'])
@login_required
def new_print():
    if request.method == 'POST':
        colors = request.form.get('colors', '').split(',')
        positions = request.form.get('positions', '').split(',')
        print_item = Print(
            name=request.form.get('name'),
            description=request.form.get('description'),
            file_url=request.form.get('file_url'),
            colors=[c.strip() for c in colors if c.strip()],
            positions=[p.strip() for p in positions if p.strip()],
            technique=request.form.get('technique', 'silk'),
            dimensions=request.form.get('dimensions'),
            active=request.form.get('active') == 'on'
        )
        db.session.add(print_item)
        db.session.commit()
        flash('Estampa criada com sucesso!', 'success')
        return redirect(url_for('prints'))
    return render_template('print_form.html', print=None)

@app.route('/prints/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_print(id):
    print_item = Print.query.get_or_404(id)
    if request.method == 'POST':
        colors = request.form.get('colors', '').split(',')
        positions = request.form.get('positions', '').split(',')
        print_item.name = request.form.get('name')
        print_item.description = request.form.get('description')
        print_item.file_url = request.form.get('file_url')
        print_item.colors = [c.strip() for c in colors if c.strip()]
        print_item.positions = [p.strip() for p in positions if p.strip()]
        print_item.technique = request.form.get('technique', 'silk')
        print_item.dimensions = request.form.get('dimensions')
        print_item.active = request.form.get('active') == 'on'
        db.session.commit()
        flash('Estampa atualizada com sucesso!', 'success')
        return redirect(url_for('prints'))
    return render_template('print_form.html', print=print_item)

@app.route('/prints/<int:id>/delete', methods=['POST'])
@login_required
def delete_print(id):
    print_item = Print.query.get_or_404(id)
    db.session.delete(print_item)
    db.session.commit()
    flash('Estampa excluída com sucesso!', 'success')
    return redirect(url_for('prints'))

@app.route('/quotes')
@login_required
def quotes():
    quotes_list = Quote.query.order_by(Quote.created_at.desc()).all()
    return render_template('quotes.html', quotes=quotes_list)

@app.route('/quotes/new', methods=['GET', 'POST'])
@login_required
def new_quote():
    if request.method == 'POST':
        quote = Quote(
            client_id=int(request.form.get('client_id')),
            seller_id=current_user.id,
            supplier_id=int(request.form.get('supplier_id')) if request.form.get('supplier_id') else None,
            items=[],
            status='pending',
            total_quantity=int(request.form.get('total_quantity', 0)),
            notes=request.form.get('notes')
        )
        db.session.add(quote)
        db.session.commit()
        flash('Cotação criada com sucesso!', 'success')
        return redirect(url_for('quotes'))
    clients = Client.query.all()
    suppliers_list = Supplier.query.all()
    return render_template('quote_form.html', quote=None, clients=clients, suppliers=suppliers_list)

@app.route('/quotes/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_quote(id):
    quote = Quote.query.get_or_404(id)
    if request.method == 'POST':
        quote.client_id = int(request.form.get('client_id'))
        quote.supplier_id = int(request.form.get('supplier_id')) if request.form.get('supplier_id') else None
        quote.status = request.form.get('status', 'pending')
        quote.total_quantity = int(request.form.get('total_quantity', 0))
        quote.unit_price = float(request.form.get('unit_price')) if request.form.get('unit_price') else None
        quote.total_price = float(request.form.get('total_price')) if request.form.get('total_price') else None
        quote.delivery_days = int(request.form.get('delivery_days')) if request.form.get('delivery_days') else None
        quote.notes = request.form.get('notes')
        db.session.commit()
        flash('Cotação atualizada com sucesso!', 'success')
        return redirect(url_for('quotes'))
    clients = Client.query.all()
    suppliers_list = Supplier.query.all()
    return render_template('quote_form.html', quote=quote, clients=clients, suppliers=suppliers_list)

@app.route('/quotes/<int:id>/delete', methods=['POST'])
@login_required
def delete_quote(id):
    quote = Quote.query.get_or_404(id)
    Budget.query.filter_by(quote_id=id).delete()
    db.session.delete(quote)
    db.session.commit()
    flash('Cotação excluída com sucesso!', 'success')
    return redirect(url_for('quotes'))

@app.route('/budgets')
@login_required
def budgets():
    budgets_list = Budget.query.order_by(Budget.created_at.desc()).all()
    return render_template('budgets.html', budgets=budgets_list)

@app.route('/budgets/new', methods=['GET', 'POST'])
@login_required
def new_budget():
    if request.method == 'POST':
        last_budget = Budget.query.order_by(Budget.id.desc()).first()
        budget_num = (last_budget.id + 1) if last_budget else 1
        budget_number = f'ORC-{budget_num:04d}'
        
        total_value = float(request.form.get('total_value', 0))
        down_payment_percent = int(request.form.get('down_payment_percent', 50))
        down_payment_value = total_value * (down_payment_percent / 100)
        
        budget = Budget(
            quote_id=int(request.form.get('quote_id')),
            client_id=int(request.form.get('client_id')),
            budget_number=budget_number,
            total_value=total_value,
            down_payment_percent=down_payment_percent,
            down_payment_value=down_payment_value,
            pix_key=request.form.get('pix_key', '11998896725'),
            status='draft',
            valid_until=datetime.utcnow() + timedelta(days=7),
            notes=request.form.get('notes')
        )
        db.session.add(budget)
        db.session.commit()
        flash('Orçamento criado com sucesso!', 'success')
        return redirect(url_for('budgets'))
    quotes_list = Quote.query.filter_by(status='approved').all()
    clients = Client.query.all()
    return render_template('budget_form.html', budget=None, quotes=quotes_list, clients=clients)

@app.route('/budgets/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_budget(id):
    budget = Budget.query.get_or_404(id)
    if request.method == 'POST':
        budget.total_value = float(request.form.get('total_value', 0))
        budget.down_payment_percent = int(request.form.get('down_payment_percent', 50))
        budget.down_payment_value = budget.total_value * (budget.down_payment_percent / 100)
        budget.pix_key = request.form.get('pix_key', '11998896725')
        budget.status = request.form.get('status', 'draft')
        budget.notes = request.form.get('notes')
        db.session.commit()
        flash('Orçamento atualizado com sucesso!', 'success')
        return redirect(url_for('budgets'))
    quotes_list = Quote.query.all()
    clients = Client.query.all()
    return render_template('budget_form.html', budget=budget, quotes=quotes_list, clients=clients)

@app.route('/budgets/<int:id>/delete', methods=['POST'])
@login_required
def delete_budget(id):
    budget = Budget.query.get_or_404(id)
    Order.query.filter_by(budget_id=id).delete()
    db.session.delete(budget)
    db.session.commit()
    flash('Orçamento excluído com sucesso!', 'success')
    return redirect(url_for('budgets'))

@app.route('/orders')
@login_required
def orders():
    orders_list = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders_list)

@app.route('/orders/new', methods=['GET', 'POST'])
@login_required
def new_order():
    if request.method == 'POST':
        last_order = Order.query.order_by(Order.id.desc()).first()
        order_num = (last_order.id + 1) if last_order else 1
        order_number = f'PED-{datetime.now().year}-{order_num:03d}'
        
        order = Order(
            budget_id=int(request.form.get('budget_id')),
            client_id=int(request.form.get('client_id')),
            supplier_id=int(request.form.get('supplier_id')),
            order_number=order_number,
            status='approved',
            production_step='cutting',
            progress=0,
            total_value=float(request.form.get('total_value', 0)),
            notes=request.form.get('notes')
        )
        db.session.add(order)
        db.session.commit()
        flash('Pedido criado com sucesso!', 'success')
        return redirect(url_for('orders'))
    budgets_list = Budget.query.filter_by(status='approved').all()
    clients = Client.query.all()
    suppliers_list = Supplier.query.all()
    return render_template('order_form.html', order=None, budgets=budgets_list, clients=clients, suppliers=suppliers_list)

@app.route('/orders/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    order = Order.query.get_or_404(id)
    if request.method == 'POST':
        order.status = request.form.get('status', 'approved')
        order.production_step = request.form.get('production_step', 'cutting')
        order.progress = int(request.form.get('progress', 0))
        order.tracking_code = request.form.get('tracking_code')
        order.notes = request.form.get('notes')
        if order.status == 'delivered' and not order.delivered_at:
            order.delivered_at = datetime.utcnow()
        db.session.commit()
        flash('Pedido atualizado com sucesso!', 'success')
        return redirect(url_for('orders'))
    budgets_list = Budget.query.all()
    clients = Client.query.all()
    suppliers_list = Supplier.query.all()
    return render_template('order_form.html', order=order, budgets=budgets_list, clients=clients, suppliers=suppliers_list)

@app.route('/orders/<int:id>/delete', methods=['POST'])
@login_required
def delete_order(id):
    order = Order.query.get_or_404(id)
    Transaction.query.filter_by(order_id=id).delete()
    db.session.delete(order)
    db.session.commit()
    flash('Pedido excluído com sucesso!', 'success')
    return redirect(url_for('orders'))

@app.route('/clients')
@login_required
def clients():
    clients_list = Client.query.order_by(Client.created_at.desc()).all()
    return render_template('clients.html', clients=clients_list)

@app.route('/clients/new', methods=['GET', 'POST'])
@login_required
def new_client():
    if request.method == 'POST':
        client = Client(
            name=request.form.get('name'),
            cpf_cnpj=request.form.get('cpf_cnpj'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            address=request.form.get('address'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            zip_code=request.form.get('zip_code')
        )
        db.session.add(client)
        db.session.commit()
        flash('Cliente criado com sucesso!', 'success')
        return redirect(url_for('clients'))
    return render_template('client_form.html', client=None)

@app.route('/clients/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_client(id):
    client = Client.query.get_or_404(id)
    if request.method == 'POST':
        client.name = request.form.get('name')
        client.cpf_cnpj = request.form.get('cpf_cnpj')
        client.email = request.form.get('email')
        client.phone = request.form.get('phone')
        client.address = request.form.get('address')
        client.city = request.form.get('city')
        client.state = request.form.get('state')
        client.zip_code = request.form.get('zip_code')
        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('clients'))
    return render_template('client_form.html', client=client)

@app.route('/clients/<int:id>/delete', methods=['POST'])
@login_required
def delete_client(id):
    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    flash('Cliente excluído com sucesso!', 'success')
    return redirect(url_for('clients'))

@app.route('/products')
@login_required
def products():
    products_list = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('products.html', products=products_list)

@app.route('/products/new', methods=['GET', 'POST'])
@login_required
def new_product():
    if request.method == 'POST':
        sizes = request.form.get('sizes', '').split(',')
        product = Product(
            name=request.form.get('name'),
            model=request.form.get('model'),
            fabric=request.form.get('fabric'),
            color=request.form.get('color'),
            sizes=[s.strip() for s in sizes if s.strip()],
            base_price=float(request.form.get('base_price', 0)),
            stock=int(request.form.get('stock', 0)),
            image_url=request.form.get('image_url'),
            active=request.form.get('active') == 'on'
        )
        db.session.add(product)
        db.session.commit()
        flash('Produto criado com sucesso!', 'success')
        return redirect(url_for('products'))
    return render_template('product_form.html', product=None)

@app.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        sizes = request.form.get('sizes', '').split(',')
        product.name = request.form.get('name')
        product.model = request.form.get('model')
        product.fabric = request.form.get('fabric')
        product.color = request.form.get('color')
        product.sizes = [s.strip() for s in sizes if s.strip()]
        product.base_price = float(request.form.get('base_price', 0))
        product.stock = int(request.form.get('stock', 0))
        product.image_url = request.form.get('image_url')
        product.active = request.form.get('active') == 'on'
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('products'))
    return render_template('product_form.html', product=product)

@app.route('/products/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('products'))

@app.route('/orders/<int:order_id>/transactions')
@login_required
def transactions(order_id):
    order = Order.query.get_or_404(order_id)
    transactions_list = Transaction.query.filter_by(order_id=order_id).order_by(Transaction.transaction_date.desc()).all()
    return render_template('transactions.html', transactions=transactions_list, order=order)

@app.route('/orders/<int:order_id>/transactions/new', methods=['GET', 'POST'])
@login_required
def new_transaction(order_id):
    order = Order.query.get_or_404(order_id)
    if request.method == 'POST':
        transaction = Transaction(
            order_id=order_id,
            payment_method=request.form.get('payment_method'),
            amount=float(request.form.get('amount', 0)),
            status=request.form.get('status', 'pending'),
            notes=request.form.get('notes')
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transação registrada com sucesso!', 'success')
        return redirect(url_for('transactions', order_id=order_id))
    return render_template('transaction_form.html', transaction=None, order=order)

@app.route('/orders/<int:order_id>/transactions/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_transaction(order_id, id):
    order = Order.query.get_or_404(order_id)
    transaction = Transaction.query.get_or_404(id)
    if request.method == 'POST':
        transaction.payment_method = request.form.get('payment_method')
        transaction.amount = float(request.form.get('amount', 0))
        transaction.status = request.form.get('status', 'pending')
        transaction.notes = request.form.get('notes')
        db.session.commit()
        flash('Transação atualizada com sucesso!', 'success')
        return redirect(url_for('transactions', order_id=order_id))
    return render_template('transaction_form.html', transaction=transaction, order=order)

@app.route('/orders/<int:order_id>/transactions/<int:id>/delete', methods=['POST'])
@login_required
def delete_transaction(order_id, id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    flash('Transação excluída com sucesso!', 'success')
    return redirect(url_for('transactions', order_id=order_id))

@app.route('/users')
@login_required
def users():
    if current_user.role != 'ADMIN':
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('dashboard'))
    users_list = User.query.order_by(User.created_at.desc()).all()
    return render_template('users.html', users=users_list)

@app.route('/users/new', methods=['GET', 'POST'])
@login_required
def new_user():
    if current_user.role != 'ADMIN':
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        existing = User.query.filter_by(email=request.form.get('email')).first()
        if existing:
            flash('Email já cadastrado', 'error')
            return render_template('user_form.html', user=None)
        user = User(
            name=request.form.get('name'),
            email=request.form.get('email'),
            role=request.form.get('role', 'SELLER'),
            phone=request.form.get('phone')
        )
        user.set_password(request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('users'))
    return render_template('user_form.html', user=None)

@app.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if current_user.role != 'ADMIN':
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('dashboard'))
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        user.role = request.form.get('role', 'SELLER')
        user.phone = request.form.get('phone')
        if request.form.get('password'):
            user.set_password(request.form.get('password'))
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('users'))
    return render_template('user_form.html', user=user)

@app.route('/users/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
    if current_user.role != 'ADMIN':
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('dashboard'))
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('Você não pode excluir seu próprio usuário', 'error')
        return redirect(url_for('users'))
    db.session.delete(user)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('users'))

@app.route('/api/metrics')
@login_required
def api_metrics():
    return jsonify(get_dashboard_metrics())

def init_db():
    with app.app_context():
        db.create_all()
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@emunah.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', os.urandom(16).hex())
        
        if not User.query.filter_by(email=admin_email).first() and not User.query.first():
            admin = User(
                name='Administrador',
                email=admin_email,
                role='ADMIN',
                phone=''
            )
            admin.set_password(admin_password)
            print(f'Admin user created: {admin_email}')
            if 'ADMIN_PASSWORD' not in os.environ:
                print(f'Generated password: {admin_password}')
                print('IMPORTANT: Set ADMIN_PASSWORD environment variable for production!')
            db.session.add(admin)
            
            supplier1 = Supplier(
                name='Confecções Premium',
                contact_name='João Silva',
                email='contato@premium.com',
                phone='11999887766',
                production_time_days=7,
                rating=4.8,
                payment_method='PIX'
            )
            supplier2 = Supplier(
                name='Têxtil Brasil',
                contact_name='Maria Santos',
                email='maria@textilbrasil.com',
                phone='11988776655',
                production_time_days=10,
                rating=4.5,
                payment_method='Boleto'
            )
            db.session.add(supplier1)
            db.session.add(supplier2)
            
            print1 = Print(
                name='Logo Emunah',
                description='Logo oficial da marca',
                colors=['Preto', 'Branco'],
                positions=['Peito', 'Costas'],
                technique='silk',
                dimensions='10x10cm',
                active=True
            )
            print2 = Print(
                name='Estampa Geométrica',
                description='Design geométrico moderno',
                colors=['Azul', 'Vermelho', 'Amarelo'],
                positions=['Costas', 'Manga'],
                technique='dtf',
                dimensions='30x40cm',
                active=True
            )
            db.session.add(print1)
            db.session.add(print2)
            
            client1 = Client(
                name='Tech Solutions LTDA',
                cpf_cnpj='12.345.678/0001-90',
                email='contato@techsolutions.com',
                phone='11987654321',
                city='São Paulo',
                state='SP'
            )
            db.session.add(client1)
            
            db.session.commit()
            print('Database initialized with sample data.')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'False') == 'True')
