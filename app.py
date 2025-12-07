import os
import smtplib
import logging
import uuid
import base64
import qrcode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, make_response
from urllib.parse import quote as url_quote
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from decimal import Decimal
import json

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.environ.get('SESSION_SECRET', 'emunah-secret-key-change-in-production'))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///emunah.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@emunah.com')

# Upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads', 'quotes')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_quote_image(file, quote_id):
    """Save uploaded image for a quote and return the relative path"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"quote_{quote_id}_{uuid.uuid4().hex[:8]}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        return f"uploads/quotes/{unique_filename}"
    return None

def delete_quote_image(image_path):
    """Delete a quote image file"""
    if image_path:
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', image_path)
        if os.path.exists(full_path):
            os.remove(full_path)


def generate_pix_qrcode(pix_key, amount=None, name="Emunah", city="Sao Paulo", description=""):
    """Generate PIX QR Code as base64 string"""
    def crc16_ccitt(data):
        crc = 0xFFFF
        for byte in data.encode('utf-8'):
            crc ^= byte << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1
                crc &= 0xFFFF
        return format(crc, '04X')
    
    def format_emv(id_code, value):
        return f"{id_code}{len(value):02d}{value}"
    
    pix_key_clean = ''.join(filter(str.isdigit, pix_key)) if pix_key.replace('+', '').isdigit() else pix_key
    
    gui = format_emv("00", "BR.GOV.BCB.PIX")
    chave = format_emv("01", pix_key_clean)
    if description:
        desc_clean = description[:25].replace(" ", "")
        desc_field = format_emv("02", desc_clean)
        merchant_account = format_emv("26", gui + chave + desc_field)
    else:
        merchant_account = format_emv("26", gui + chave)
    
    payload_format = format_emv("00", "01")
    merchant_category = format_emv("52", "0000")
    currency = format_emv("53", "986")
    
    amount_field = ""
    if amount and float(amount) > 0:
        amount_str = f"{float(amount):.2f}"
        amount_field = format_emv("54", amount_str)
    
    country = format_emv("58", "BR")
    
    name_clean = name[:25].upper()
    for char in ['Á', 'À', 'Ã', 'Â', 'É', 'È', 'Ê', 'Í', 'Ì', 'Î', 'Ó', 'Ò', 'Õ', 'Ô', 'Ú', 'Ù', 'Û', 'Ç']:
        replacement = {'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A', 'É': 'E', 'È': 'E', 'Ê': 'E', 
                      'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ó': 'O', 'Ò': 'O', 'Õ': 'O', 'Ô': 'O',
                      'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ç': 'C'}.get(char, char)
        name_clean = name_clean.replace(char, replacement)
    merchant_name = format_emv("59", name_clean)
    
    city_clean = city[:15].upper()
    for char in ['Á', 'À', 'Ã', 'Â', 'É', 'È', 'Ê', 'Í', 'Ì', 'Î', 'Ó', 'Ò', 'Õ', 'Ô', 'Ú', 'Ù', 'Û', 'Ç']:
        replacement = {'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A', 'É': 'E', 'È': 'E', 'Ê': 'E', 
                      'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ó': 'O', 'Ò': 'O', 'Õ': 'O', 'Ô': 'O',
                      'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ç': 'C'}.get(char, char)
        city_clean = city_clean.replace(char, replacement)
    merchant_city = format_emv("60", city_clean)
    
    additional_data = format_emv("62", format_emv("05", "***"))
    
    payload_without_crc = payload_format + merchant_account + merchant_category + currency + amount_field + country + merchant_name + merchant_city + additional_data + "6304"
    crc = crc16_ccitt(payload_without_crc)
    payload = payload_without_crc + crc
    
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#520B1B", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return f"data:image/png;base64,{qr_base64}"


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'


# ==================== MODELS ====================

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
    quote_number = db.Column(db.String(50), unique=True)
    
    # Client - can be optional (for leads/prospects)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    
    # Lead info - used when no registered client
    lead_name = db.Column(db.String(255))
    lead_email = db.Column(db.String(255))
    lead_phone = db.Column(db.String(50))
    
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    print_id = db.Column(db.Integer, db.ForeignKey('prints.id'))
    
    # Order details
    items = db.Column(db.JSON, nullable=False, default=list)
    model = db.Column(db.String(100))
    shirt_color = db.Column(db.String(50))
    print_position = db.Column(db.String(100))
    print_size = db.Column(db.String(50))
    print_color = db.Column(db.String(50))
    
    # Pricing
    total_quantity = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Numeric(10, 2))
    total_price = db.Column(db.Numeric(10, 2))
    down_payment_percent = db.Column(db.Integer, default=40)
    down_payment_value = db.Column(db.Numeric(10, 2))
    pix_key = db.Column(db.String(100), default='11998896725')
    
    # Status: draft, pending, sent, approved, rejected, expired, converted
    status = db.Column(db.String(50), default='draft')
    
    # Delivery
    delivery_method = db.Column(db.String(50), default='delivery')  # delivery or pickup
    delivery_days = db.Column(db.Integer)
    delivery_date_estimated = db.Column(db.DateTime)
    
    # Validity
    valid_until = db.Column(db.DateTime)
    
    # Image and reference URL
    reference_url = db.Column(db.String(500))  # External link/URL
    image_path = db.Column(db.String(500))     # Path to uploaded image
    
    # Timestamps
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime)
    approved_at = db.Column(db.DateTime)
    
    # Relationships
    client = db.relationship('Client', backref='quotes')
    seller = db.relationship('User', backref='quotes')
    supplier = db.relationship('Supplier', backref='quotes')
    product = db.relationship('Product', backref='quotes')
    print_ref = db.relationship('Print', backref='quotes')
    
    def get_client_name(self):
        if self.client:
            return self.client.name
        return self.lead_name or 'Cliente não informado'
    
    def get_client_email(self):
        if self.client:
            return self.client.email
        return self.lead_email
    
    def get_client_phone(self):
        if self.client:
            return self.client.phone
        return self.lead_phone


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    
    # Lead info - copied from quote if no client
    lead_name = db.Column(db.String(255))
    lead_email = db.Column(db.String(255))
    lead_phone = db.Column(db.String(50))
    
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    
    # Status: created, production, ready, shipping, delivered, cancelled
    status = db.Column(db.String(50), default='created')
    
    # Production: cutting, printing, finishing, quality_check, ready
    production_step = db.Column(db.String(50), default='cutting')
    progress = db.Column(db.Integer, default=0)
    
    # Values
    total_value = db.Column(db.Numeric(10, 2), nullable=False)
    paid_value = db.Column(db.Numeric(10, 2), default=0)
    
    # Delivery
    delivery_method = db.Column(db.String(50), default='delivery')
    delivery_date_estimated = db.Column(db.DateTime)
    delivery_date_actual = db.Column(db.DateTime)
    tracking_code = db.Column(db.String(100))
    
    # Reference URL
    reference_url = db.Column(db.String(500))  # External link/URL
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    delivered_at = db.Column(db.DateTime)

    quote = db.relationship('Quote', backref='orders')
    client = db.relationship('Client', backref='orders')
    supplier = db.relationship('Supplier', backref='orders')
    
    def get_client_name(self):
        if self.client:
            return self.client.name
        return self.lead_name or 'Cliente não informado'
    
    def get_client_email(self):
        if self.client:
            return self.client.email
        return self.lead_email


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    print_id = db.Column(db.Integer, db.ForeignKey('prints.id'))
    
    description = db.Column(db.String(500))
    size = db.Column(db.String(20))
    color = db.Column(db.String(50))
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Numeric(10, 2))
    total_price = db.Column(db.Numeric(10, 2))
    customization = db.Column(db.JSON)
    
    order = db.relationship('Order', backref='items')
    product = db.relationship('Product', backref='order_items')
    print_ref = db.relationship('Print', backref='order_items')


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


class EmailLog(db.Model):
    __tablename__ = 'email_logs'
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(500))
    email_type = db.Column(db.String(50))
    status = db.Column(db.String(50), default='sent')
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==================== EMAIL SERVICE ====================

def send_email(to_email, subject, html_content, email_type='general'):
    """Send email using SMTP configuration"""
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        logging.warning(f"Email not configured. Would send to {to_email}: {subject}")
        email_log = EmailLog(
            recipient=to_email,
            subject=subject,
            email_type=email_type,
            status='skipped',
            error_message='Email not configured'
        )
        db.session.add(email_log)
        db.session.commit()
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = app.config['MAIL_DEFAULT_SENDER']
        msg['To'] = to_email
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        server.starttls()
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        server.sendmail(app.config['MAIL_DEFAULT_SENDER'], to_email, msg.as_string())
        server.quit()
        
        email_log = EmailLog(
            recipient=to_email,
            subject=subject,
            email_type=email_type,
            status='sent'
        )
        db.session.add(email_log)
        db.session.commit()
        
        logging.info(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email to {to_email}: {str(e)}")
        email_log = EmailLog(
            recipient=to_email,
            subject=subject,
            email_type=email_type,
            status='failed',
            error_message=str(e)
        )
        db.session.add(email_log)
        db.session.commit()
        return False


def send_quote_email(quote, to_client=True):
    """Send quote notification email"""
    if to_client:
        email = quote.get_client_email()
        if not email:
            return False
        subject = f"Emunah - Orçamento #{quote.quote_number}"
        html = f"""
        <html>
        <body style="font-family: 'Inter', Arial, sans-serif; background-color: #F5EDE6; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <h1 style="color: #520B1B; font-family: 'Playfair Display', serif;">Emunah</h1>
                    <p style="color: #666;">Vista-se com propósito</p>
                </div>
                <h2 style="color: #520B1B;">Orçamento #{quote.quote_number}</h2>
                <p>Olá {quote.get_client_name()},</p>
                <p>Segue o orçamento solicitado:</p>
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                    <tr style="background: #F5EDE6;">
                        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Modelo</strong></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{quote.model or 'Camiseta'}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Quantidade</strong></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{quote.total_quantity}</td>
                    </tr>
                    <tr style="background: #F5EDE6;">
                        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Valor Total</strong></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">R$ {quote.total_price or 0:.2f}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Sinal ({quote.down_payment_percent}%)</strong></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">R$ {quote.down_payment_value or 0:.2f}</td>
                    </tr>
                    <tr style="background: #F5EDE6;">
                        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Prazo de Entrega</strong></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{quote.delivery_days or 'A definir'} dias</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Validade</strong></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{quote.valid_until.strftime('%d/%m/%Y') if quote.valid_until else 'A definir'}</td>
                    </tr>
                </table>
                <div style="background: #F5EDE6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>PIX para pagamento:</strong> {quote.pix_key}</p>
                </div>
                <p style="color: #666; font-size: 12px;">
                    O pagamento restante deverá ser quitado no ato da entrega.
                </p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="color: #666; font-size: 12px; text-align: center;">
                    Emunah - Vista-se com propósito<br>
                    Contato: 11998896725
                </p>
            </div>
        </body>
        </html>
        """
        return send_email(email, subject, html, 'quote_sent')
    return False


def send_order_confirmation_email(order, to_client=True, to_supplier=False):
    """Send order confirmation email"""
    emails_sent = []
    
    if to_client:
        email = order.get_client_email()
        if email:
            subject = f"Emunah - Pedido #{order.order_number} Confirmado"
            html = f"""
            <html>
            <body style="font-family: 'Inter', Arial, sans-serif; background-color: #F5EDE6; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <h1 style="color: #520B1B; font-family: 'Playfair Display', serif;">Emunah</h1>
                        <p style="color: #666;">Vista-se com propósito</p>
                    </div>
                    <h2 style="color: #520B1B;">Pedido Confirmado!</h2>
                    <p>Olá {order.get_client_name()},</p>
                    <p>Seu pedido <strong>#{order.order_number}</strong> foi confirmado e está em produção!</p>
                    <div style="background: #F5EDE6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Valor Total:</strong> R$ {order.total_value:.2f}</p>
                        <p><strong>Previsão de Entrega:</strong> {order.delivery_date_estimated.strftime('%d/%m/%Y') if order.delivery_date_estimated else 'A definir'}</p>
                        <p><strong>Método:</strong> {'Entrega' if order.delivery_method == 'delivery' else 'Retirada'}</p>
                    </div>
                    <p>Você receberá atualizações sobre o andamento do seu pedido.</p>
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    <p style="color: #666; font-size: 12px; text-align: center;">
                        Emunah - Vista-se com propósito<br>
                        Contato: 11998896725
                    </p>
                </div>
            </body>
            </html>
            """
            if send_email(email, subject, html, 'order_confirmation'):
                emails_sent.append(email)
    
    if to_supplier and order.supplier:
        supplier_email = order.supplier.email
        if supplier_email:
            subject = f"Emunah - Novo Pedido #{order.order_number}"
            html = f"""
            <html>
            <body style="font-family: 'Inter', Arial, sans-serif; background-color: #F5EDE6; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <h1 style="color: #520B1B; font-family: 'Playfair Display', serif;">Emunah</h1>
                    </div>
                    <h2 style="color: #520B1B;">Novo Pedido Recebido</h2>
                    <p>Olá {order.supplier.contact_name or order.supplier.name},</p>
                    <p>Você recebeu um novo pedido da Emunah:</p>
                    <div style="background: #F5EDE6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Pedido:</strong> #{order.order_number}</p>
                        <p><strong>Cliente:</strong> {order.get_client_name()}</p>
                        <p><strong>Valor:</strong> R$ {order.total_value:.2f}</p>
                        <p><strong>Data de Entrega:</strong> {order.delivery_date_estimated.strftime('%d/%m/%Y') if order.delivery_date_estimated else 'A definir'}</p>
                    </div>
                    <p>Por favor, inicie a produção o mais breve possível.</p>
                </div>
            </body>
            </html>
            """
            if send_email(supplier_email, subject, html, 'order_supplier_notification'):
                emails_sent.append(supplier_email)
    
    return emails_sent


def send_delivery_notification(order):
    """Send delivery/pickup notification"""
    email = order.get_client_email()
    if not email:
        return False
    
    if order.delivery_method == 'pickup':
        subject = f"Emunah - Pedido #{order.order_number} Pronto para Retirada"
        message = "Seu pedido está pronto para retirada!"
    else:
        subject = f"Emunah - Pedido #{order.order_number} Saiu para Entrega"
        message = "Seu pedido saiu para entrega!"
    
    html = f"""
    <html>
    <body style="font-family: 'Inter', Arial, sans-serif; background-color: #F5EDE6; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="color: #520B1B; font-family: 'Playfair Display', serif;">Emunah</h1>
                <p style="color: #666;">Vista-se com propósito</p>
            </div>
            <h2 style="color: #520B1B;">{message}</h2>
            <p>Olá {order.get_client_name()},</p>
            <p>{message}</p>
            <div style="background: #F5EDE6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Pedido:</strong> #{order.order_number}</p>
                {'<p><strong>Código de Rastreio:</strong> ' + order.tracking_code + '</p>' if order.tracking_code else ''}
            </div>
            <p>Agradecemos a preferência!</p>
            <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
            <p style="color: #666; font-size: 12px; text-align: center;">
                Emunah - Vista-se com propósito<br>
                Contato: 11998896725
            </p>
        </div>
    </body>
    </html>
    """
    return send_email(email, subject, html, 'delivery_notification')


# ==================== USER LOADER ====================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==================== HELPERS ====================

def get_dashboard_metrics():
    total_revenue = db.session.query(db.func.coalesce(db.func.sum(Order.total_value), 0)).filter(Order.status == 'delivered').scalar()
    completed_orders = Order.query.filter_by(status='delivered').count()
    pending_quotes = Quote.query.filter(Quote.status.in_(['draft', 'pending', 'sent'])).count()
    avg_ticket = db.session.query(db.func.coalesce(db.func.avg(Order.total_value), 0)).filter(Order.status == 'delivered').scalar()
    orders_in_production = Order.query.filter_by(status='production').count()
    return {
        'total_revenue': float(total_revenue) if total_revenue else 0,
        'completed_orders': completed_orders,
        'pending_quotes': pending_quotes,
        'average_ticket': float(avg_ticket) if avg_ticket else 0,
        'orders_in_production': orders_in_production
    }


def generate_quote_number():
    last_quote = Quote.query.order_by(Quote.id.desc()).first()
    num = (last_quote.id + 1) if last_quote else 1
    return f'ORC-{datetime.now().year}-{num:04d}'


def generate_order_number():
    last_order = Order.query.order_by(Order.id.desc()).first()
    num = (last_order.id + 1) if last_order else 1
    return f'PED-{datetime.now().year}-{num:04d}'


# ==================== ROUTES ====================

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
    quotes = Quote.query.order_by(Quote.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', metrics=metrics, orders=orders, quotes=quotes)


# ==================== QUOTES ====================

@app.route('/quotes')
@login_required
def quotes():
    status_filter = request.args.get('status', '')
    query = Quote.query.order_by(Quote.created_at.desc())
    if status_filter:
        query = query.filter_by(status=status_filter)
    quotes_list = query.all()
    return render_template('quotes.html', quotes=quotes_list, current_status=status_filter)


@app.route('/quotes/new', methods=['GET', 'POST'])
@login_required
def new_quote():
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        
        # Calculate prices - handle empty strings properly
        total_quantity_str = request.form.get('total_quantity', '0')
        total_quantity = int(total_quantity_str) if total_quantity_str else 0
        
        unit_price_str = request.form.get('unit_price', '')
        unit_price = float(unit_price_str) if unit_price_str else 0
        
        total_price_str = request.form.get('total_price', '')
        total_price = total_quantity * unit_price if unit_price else (float(total_price_str) if total_price_str else 0)
        
        down_payment_percent_str = request.form.get('down_payment_percent', '40')
        down_payment_percent = int(down_payment_percent_str) if down_payment_percent_str else 40
        down_payment_value = total_price * (down_payment_percent / 100)
        
        # Calculate delivery date
        delivery_days = int(request.form.get('delivery_days', 15)) if request.form.get('delivery_days') else 15
        delivery_date = datetime.utcnow() + timedelta(days=delivery_days)
        
        quote = Quote(
            quote_number=generate_quote_number(),
            client_id=int(client_id) if client_id else None,
            lead_name=request.form.get('lead_name') if not client_id else None,
            lead_email=request.form.get('lead_email') if not client_id else None,
            lead_phone=request.form.get('lead_phone') if not client_id else None,
            seller_id=current_user.id,
            supplier_id=int(request.form.get('supplier_id')) if request.form.get('supplier_id') else None,
            product_id=int(request.form.get('product_id')) if request.form.get('product_id') else None,
            print_id=int(request.form.get('print_id')) if request.form.get('print_id') else None,
            model=request.form.get('model', 'Camiseta'),
            shirt_color=request.form.get('shirt_color'),
            print_position=request.form.get('print_position'),
            print_size=request.form.get('print_size'),
            print_color=request.form.get('print_color'),
            total_quantity=total_quantity,
            unit_price=unit_price if unit_price else None,
            total_price=total_price if total_price else None,
            down_payment_percent=down_payment_percent,
            down_payment_value=down_payment_value if down_payment_value else None,
            pix_key=request.form.get('pix_key', '11998896725'),
            delivery_method=request.form.get('delivery_method', 'delivery'),
            delivery_days=delivery_days,
            delivery_date_estimated=delivery_date,
            valid_until=datetime.utcnow() + timedelta(days=15),
            status='draft',
            items=[],
            notes=request.form.get('notes'),
            reference_url=request.form.get('reference_url')
        )
        db.session.add(quote)
        db.session.commit()
        
        # Handle image upload after quote is created (to get the ID)
        if 'quote_image' in request.files:
            file = request.files['quote_image']
            if file and file.filename:
                image_path = save_quote_image(file, quote.id)
                if image_path:
                    quote.image_path = image_path
                    db.session.commit()
        
        flash('Cotação criada com sucesso!', 'success')
        return redirect(url_for('view_quote', id=quote.id))
    
    clients = Client.query.order_by(Client.name).all()
    suppliers_list = Supplier.query.order_by(Supplier.name).all()
    products = Product.query.filter_by(active=True).all()
    prints = Print.query.filter_by(active=True).all()
    return render_template('quote_form.html', quote=None, clients=clients, 
                          suppliers=suppliers_list, products=products, prints=prints)


@app.route('/quotes/<int:id>')
@login_required
def view_quote(id):
    quote = Quote.query.get_or_404(id)
    return render_template('quote_view.html', quote=quote)


@app.route('/quotes/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_quote(id):
    quote = Quote.query.get_or_404(id)
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        quote.client_id = int(client_id) if client_id else None
        quote.lead_name = request.form.get('lead_name') if not client_id else None
        quote.lead_email = request.form.get('lead_email') if not client_id else None
        quote.lead_phone = request.form.get('lead_phone') if not client_id else None
        quote.supplier_id = int(request.form.get('supplier_id')) if request.form.get('supplier_id') else None
        quote.product_id = int(request.form.get('product_id')) if request.form.get('product_id') else None
        quote.print_id = int(request.form.get('print_id')) if request.form.get('print_id') else None
        quote.model = request.form.get('model', 'Camiseta')
        quote.shirt_color = request.form.get('shirt_color')
        quote.print_position = request.form.get('print_position')
        quote.print_size = request.form.get('print_size')
        quote.print_color = request.form.get('print_color')
        total_qty_str = request.form.get('total_quantity', '0')
        quote.total_quantity = int(total_qty_str) if total_qty_str else 0
        
        unit_price_str = request.form.get('unit_price', '')
        quote.unit_price = float(unit_price_str) if unit_price_str else None
        
        total_price_str = request.form.get('total_price', '')
        quote.total_price = float(total_price_str) if total_price_str else None
        
        down_pmt_str = request.form.get('down_payment_percent', '40')
        quote.down_payment_percent = int(down_pmt_str) if down_pmt_str else 40
        if quote.total_price:
            quote.down_payment_value = float(quote.total_price) * (quote.down_payment_percent / 100)
        quote.pix_key = request.form.get('pix_key', '11998896725')
        quote.delivery_method = request.form.get('delivery_method', 'delivery')
        delivery_days_str = request.form.get('delivery_days', '')
        quote.delivery_days = int(delivery_days_str) if delivery_days_str else None
        if quote.delivery_days:
            quote.delivery_date_estimated = datetime.utcnow() + timedelta(days=quote.delivery_days)
        quote.status = request.form.get('status', quote.status)
        quote.notes = request.form.get('notes')
        quote.reference_url = request.form.get('reference_url')
        
        # Handle image upload
        if 'quote_image' in request.files:
            file = request.files['quote_image']
            if file and file.filename:
                # Delete old image if exists
                if quote.image_path:
                    delete_quote_image(quote.image_path)
                # Save new image
                image_path = save_quote_image(file, quote.id)
                if image_path:
                    quote.image_path = image_path
        
        # Handle image deletion
        if request.form.get('delete_image') == '1' and quote.image_path:
            delete_quote_image(quote.image_path)
            quote.image_path = None
        
        db.session.commit()
        flash('Cotação atualizada com sucesso!', 'success')
        return redirect(url_for('view_quote', id=quote.id))
    
    clients = Client.query.order_by(Client.name).all()
    suppliers_list = Supplier.query.order_by(Supplier.name).all()
    products = Product.query.filter_by(active=True).all()
    prints = Print.query.filter_by(active=True).all()
    return render_template('quote_form.html', quote=quote, clients=clients, 
                          suppliers=suppliers_list, products=products, prints=prints)


@app.route('/quotes/<int:id>/send', methods=['POST'])
@login_required
def send_quote(id):
    quote = Quote.query.get_or_404(id)
    quote.status = 'sent'
    quote.sent_at = datetime.utcnow()
    db.session.commit()
    
    # Send email to client
    if send_quote_email(quote, to_client=True):
        flash('Cotação enviada por email com sucesso!', 'success')
    else:
        flash('Cotação marcada como enviada. (Email não configurado)', 'info')
    
    return redirect(url_for('view_quote', id=quote.id))


@app.route('/quotes/<int:id>/approve', methods=['POST'])
@login_required
def approve_quote(id):
    """Approve quote and automatically create order"""
    quote = Quote.query.get_or_404(id)
    
    if quote.status == 'converted':
        flash('Esta cotação já foi convertida em pedido.', 'warning')
        return redirect(url_for('view_quote', id=quote.id))
    
    # Update quote status
    quote.status = 'approved'
    quote.approved_at = datetime.utcnow()
    
    # Create order from quote
    order = Order(
        quote_id=quote.id,
        client_id=quote.client_id,
        supplier_id=quote.supplier_id,
        lead_name=quote.lead_name,
        lead_email=quote.lead_email,
        lead_phone=quote.lead_phone,
        order_number=generate_order_number(),
        status='created',
        production_step='cutting',
        progress=0,
        total_value=quote.total_price or 0,
        paid_value=quote.down_payment_value or 0,
        delivery_method=quote.delivery_method,
        delivery_date_estimated=quote.delivery_date_estimated,
        notes=quote.notes,
        reference_url=quote.reference_url
    )
    db.session.add(order)
    
    # Mark quote as converted
    quote.status = 'converted'
    
    db.session.commit()
    
    # Send confirmation emails
    emails = send_order_confirmation_email(order, to_client=True, to_supplier=True)
    if emails:
        flash(f'Pedido #{order.order_number} criado! Emails enviados para: {", ".join(emails)}', 'success')
    else:
        flash(f'Pedido #{order.order_number} criado com sucesso!', 'success')
    
    return redirect(url_for('view_order', id=order.id))


@app.route('/quotes/<int:id>/reject', methods=['POST'])
@login_required
def reject_quote(id):
    quote = Quote.query.get_or_404(id)
    quote.status = 'rejected'
    db.session.commit()
    flash('Cotação rejeitada.', 'info')
    return redirect(url_for('quotes'))


@app.route('/quotes/<int:id>/delete', methods=['POST'])
@login_required
def delete_quote(id):
    quote = Quote.query.get_or_404(id)
    db.session.delete(quote)
    db.session.commit()
    flash('Cotação excluída com sucesso!', 'success')
    return redirect(url_for('quotes'))


@app.route('/quotes/<int:id>/pdf')
@login_required
def download_quote_pdf(id):
    """Generate and download quote as PDF"""
    from weasyprint import HTML, CSS
    
    quote = Quote.query.get_or_404(id)
    
    logo_path = os.path.join(app.root_path, 'static', 'images', 'logo_emunah.png')
    if not os.path.exists(logo_path):
        logo_path = os.path.join(app.root_path, 'static', 'images', 'logo.png')
    
    logo_url = f"file://{logo_path}"
    
    pix_qr_path = os.path.join(app.root_path, 'static', 'images', 'pix_qrcode.png')
    if os.path.exists(pix_qr_path):
        pix_qr_code = f"file://{pix_qr_path}"
    else:
        pix_qr_code = generate_pix_qrcode(
            pix_key=quote.pix_key or '11998896725',
            amount=float(quote.down_payment_value) if quote.down_payment_value else None,
            name="Emunah",
            city="Sao Paulo",
            description=f"ORC{quote.quote_number}"
        )
    
    quote_image_url = None
    if quote.image_path:
        quote_image_path = os.path.join(app.root_path, 'static', quote.image_path)
        if os.path.exists(quote_image_path):
            quote_image_url = f"file://{quote_image_path}"
    
    html_content = render_template('quote_pdf.html', 
                                   quote=quote, 
                                   logo_path=logo_url,
                                   pix_qr_code=pix_qr_code,
                                   quote_image_url=quote_image_url)
    
    pdf_buffer = BytesIO()
    HTML(string=html_content, base_url=app.root_path).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    
    filename = f"Orcamento_{quote.quote_number.replace('-', '_')}.pdf"
    
    response = make_response(pdf_buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@app.route('/quotes/<int:id>/whatsapp')
@login_required
def share_quote_whatsapp(id):
    """Generate WhatsApp share link for quote"""
    quote = Quote.query.get_or_404(id)
    
    client_name = quote.get_client_name()
    client_phone = quote.get_client_phone()
    
    message = f"""🙏 *EMUNAH - Vista-se com propósito*

Olá {client_name}! 

Segue o orçamento solicitado:

📋 *Orçamento #{quote.quote_number}*

📦 *Produto:* {quote.model or 'Camiseta Personalizada'}
🎨 *Cor:* {quote.shirt_color or 'A definir'}
📐 *Quantidade:* {quote.total_quantity} peças

💰 *Valor Total:* R$ {quote.total_price or 0:.2f}
💳 *Sinal ({quote.down_payment_percent}%):* R$ {quote.down_payment_value or 0:.2f}
📅 *Prazo:* {quote.delivery_days or 15} dias úteis

🔑 *PIX para pagamento:* {quote.pix_key}

O restante será pago na {'entrega' if quote.delivery_method == 'delivery' else 'retirada'}.

✨ _"Tudo posso naquele que me fortalece." - Filipenses 4:13_

Ficamos à disposição para qualquer dúvida!
*Emunah* 🙏"""

    encoded_message = url_quote(message)
    
    if client_phone:
        phone = ''.join(filter(str.isdigit, client_phone))
        if not phone.startswith('55'):
            phone = '55' + phone
        whatsapp_url = f"https://wa.me/{phone}?text={encoded_message}"
    else:
        whatsapp_url = f"https://wa.me/?text={encoded_message}"
    
    return redirect(whatsapp_url)


@app.route('/quotes/<int:id>/email-pdf', methods=['POST'])
@login_required
def email_quote_pdf(id):
    """Send quote PDF via email"""
    from weasyprint import HTML
    
    quote = Quote.query.get_or_404(id)
    client_email = quote.get_client_email()
    
    if not client_email:
        flash('Cliente não possui email cadastrado.', 'error')
        return redirect(url_for('view_quote', id=quote.id))
    
    logo_path = os.path.join(app.root_path, 'static', 'images', 'logo_emunah.png')
    if not os.path.exists(logo_path):
        logo_path = os.path.join(app.root_path, 'static', 'images', 'logo.png')
    
    logo_url = f"file://{logo_path}"
    
    html_content = render_template('quote_pdf.html', quote=quote, logo_path=logo_url)
    
    pdf_buffer = BytesIO()
    HTML(string=html_content, base_url=app.root_path).write_pdf(pdf_buffer)
    pdf_data = pdf_buffer.getvalue()
    
    subject = f"Emunah - Orçamento #{quote.quote_number}"
    
    email_html = f"""
    <html>
    <body style="font-family: 'Inter', Arial, sans-serif; background-color: #F5EDE6; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="color: #520B1B; font-family: 'Playfair Display', serif;">Emunah</h1>
                <p style="color: #666;">Vista-se com propósito</p>
            </div>
            <h2 style="color: #520B1B;">Orçamento #{quote.quote_number}</h2>
            <p>Olá {quote.get_client_name()},</p>
            <p>Segue em anexo o orçamento solicitado.</p>
            <div style="background: #F5EDE6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Valor Total:</strong> R$ {quote.total_price or 0:.2f}</p>
                <p><strong>Sinal ({quote.down_payment_percent}%):</strong> R$ {quote.down_payment_value or 0:.2f}</p>
                <p><strong>Prazo:</strong> {quote.delivery_days or 15} dias úteis</p>
            </div>
            <p><strong>PIX para pagamento:</strong> {quote.pix_key}</p>
            <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
            <p style="font-style: italic; color: #520B1B; text-align: center;">
                "Tudo posso naquele que me fortalece." - Filipenses 4:13
            </p>
            <p style="color: #666; font-size: 12px; text-align: center;">
                Emunah - Vista-se com propósito<br>
                Contato: (11) 99889-6725
            </p>
        </div>
    </body>
    </html>
    """
    
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        flash('Configuração de email não encontrada. Baixe o PDF e envie manualmente.', 'warning')
        return redirect(url_for('view_quote', id=quote.id))
    
    try:
        from email.mime.base import MIMEBase
        from email import encoders
        
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = app.config['MAIL_DEFAULT_SENDER']
        msg['To'] = client_email
        
        msg.attach(MIMEText(email_html, 'html'))
        
        pdf_attachment = MIMEBase('application', 'pdf')
        pdf_attachment.set_payload(pdf_data)
        encoders.encode_base64(pdf_attachment)
        pdf_attachment.add_header('Content-Disposition', f'attachment; filename="Orcamento_{quote.quote_number}.pdf"')
        msg.attach(pdf_attachment)
        
        server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        server.starttls()
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        server.sendmail(app.config['MAIL_DEFAULT_SENDER'], client_email, msg.as_string())
        server.quit()
        
        quote.status = 'sent'
        quote.sent_at = datetime.utcnow()
        db.session.commit()
        
        email_log = EmailLog(
            recipient=client_email,
            subject=subject,
            email_type='quote_pdf',
            status='sent'
        )
        db.session.add(email_log)
        db.session.commit()
        
        flash(f'Orçamento enviado por email para {client_email} com sucesso!', 'success')
        
    except Exception as e:
        logging.error(f"Failed to send email with PDF to {client_email}: {str(e)}")
        email_log = EmailLog(
            recipient=client_email,
            subject=subject,
            email_type='quote_pdf',
            status='failed',
            error_message=str(e)
        )
        db.session.add(email_log)
        db.session.commit()
        flash(f'Erro ao enviar email: {str(e)}. Baixe o PDF e envie manualmente.', 'error')
    
    return redirect(url_for('view_quote', id=quote.id))


# ==================== ORDERS ====================

@app.route('/orders')
@login_required
def orders():
    status_filter = request.args.get('status', '')
    query = Order.query.order_by(Order.created_at.desc())
    if status_filter:
        query = query.filter_by(status=status_filter)
    orders_list = query.all()
    return render_template('orders.html', orders=orders_list, current_status=status_filter)


@app.route('/orders/<int:id>')
@login_required
def view_order(id):
    order = Order.query.get_or_404(id)
    return render_template('order_view.html', order=order)


@app.route('/orders/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    order = Order.query.get_or_404(id)
    old_status = order.status
    
    if request.method == 'POST':
        order.status = request.form.get('status', 'created')
        order.production_step = request.form.get('production_step', 'cutting')
        order.progress = int(request.form.get('progress', 0))
        order.tracking_code = request.form.get('tracking_code')
        order.delivery_method = request.form.get('delivery_method', 'delivery')
        
        if request.form.get('delivery_date_estimated'):
            order.delivery_date_estimated = datetime.strptime(request.form.get('delivery_date_estimated'), '%Y-%m-%d')
        
        order.notes = request.form.get('notes')
        
        # Check status changes for notifications
        if order.status == 'delivered' and old_status != 'delivered':
            order.delivered_at = datetime.utcnow()
            order.delivery_date_actual = datetime.utcnow()
        
        if order.status in ['ready', 'shipping'] and old_status not in ['ready', 'shipping', 'delivered']:
            send_delivery_notification(order)
        
        db.session.commit()
        flash('Pedido atualizado com sucesso!', 'success')
        return redirect(url_for('view_order', id=order.id))
    
    return render_template('order_form.html', order=order)


@app.route('/orders/<int:id>/update-status', methods=['POST'])
@login_required
def update_order_status(id):
    order = Order.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status:
        old_status = order.status
        order.status = new_status
        
        # Update production step based on status
        if new_status == 'production':
            order.production_step = request.form.get('production_step', 'cutting')
        elif new_status == 'ready':
            order.production_step = 'ready'
            order.progress = 100
        elif new_status == 'delivered':
            order.delivered_at = datetime.utcnow()
            order.delivery_date_actual = datetime.utcnow()
            order.progress = 100
        
        # Send notification on ready/shipping
        if new_status in ['ready', 'shipping'] and old_status not in ['ready', 'shipping', 'delivered']:
            if send_delivery_notification(order):
                flash('Notificação enviada ao cliente!', 'success')
        
        db.session.commit()
        flash(f'Status atualizado para: {new_status}', 'success')
    
    return redirect(url_for('view_order', id=order.id))


@app.route('/orders/<int:id>/delete', methods=['POST'])
@login_required
def delete_order(id):
    order = Order.query.get_or_404(id)
    OrderItem.query.filter_by(order_id=id).delete()
    Transaction.query.filter_by(order_id=id).delete()
    db.session.delete(order)
    db.session.commit()
    flash('Pedido excluído com sucesso!', 'success')
    return redirect(url_for('orders'))


# ==================== SUPPLIERS ====================

@app.route('/suppliers')
@login_required
def suppliers():
    suppliers_list = Supplier.query.order_by(Supplier.name).all()
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


# ==================== PRINTS ====================

@app.route('/prints')
@login_required
def prints():
    prints_list = Print.query.order_by(Print.name).all()
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


# ==================== CLIENTS ====================

@app.route('/clients')
@login_required
def clients():
    clients_list = Client.query.order_by(Client.name).all()
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


# ==================== PRODUCTS ====================

@app.route('/products')
@login_required
def products():
    products_list = Product.query.order_by(Product.name).all()
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


# ==================== TRANSACTIONS ====================

@app.route('/orders/<int:order_id>/transactions')
@login_required
def transactions(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('transactions.html', order=order)


@app.route('/orders/<int:order_id>/transactions/new', methods=['GET', 'POST'])
@login_required
def new_transaction(order_id):
    order = Order.query.get_or_404(order_id)
    if request.method == 'POST':
        amount = float(request.form.get('amount', 0))
        transaction = Transaction(
            order_id=order_id,
            payment_method=request.form.get('payment_method'),
            amount=amount,
            status=request.form.get('status', 'pending'),
            notes=request.form.get('notes')
        )
        db.session.add(transaction)
        
        # Update order paid value
        if transaction.status == 'confirmed':
            order.paid_value = float(order.paid_value or 0) + amount
        
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
        old_amount = float(transaction.amount) if transaction.status == 'confirmed' else 0
        transaction.payment_method = request.form.get('payment_method')
        transaction.amount = float(request.form.get('amount', 0))
        transaction.status = request.form.get('status', 'pending')
        transaction.notes = request.form.get('notes')
        
        # Update order paid value
        new_amount = float(transaction.amount) if transaction.status == 'confirmed' else 0
        order.paid_value = float(order.paid_value or 0) - old_amount + new_amount
        
        db.session.commit()
        flash('Transação atualizada com sucesso!', 'success')
        return redirect(url_for('transactions', order_id=order_id))
    return render_template('transaction_form.html', transaction=transaction, order=order)


@app.route('/orders/<int:order_id>/transactions/<int:id>/delete', methods=['POST'])
@login_required
def delete_transaction(order_id, id):
    transaction = Transaction.query.get_or_404(id)
    order = Order.query.get_or_404(order_id)
    
    if transaction.status == 'confirmed':
        order.paid_value = float(order.paid_value or 0) - float(transaction.amount)
    
    db.session.delete(transaction)
    db.session.commit()
    flash('Transação excluída com sucesso!', 'success')
    return redirect(url_for('transactions', order_id=order_id))


# ==================== USERS ====================

@app.route('/users')
@login_required
def users():
    if current_user.role != 'ADMIN':
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('dashboard'))
    users_list = User.query.order_by(User.name).all()
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


# ==================== API ====================

@app.route('/api/metrics')
@login_required
def api_metrics():
    return jsonify(get_dashboard_metrics())


# ==================== INIT ====================

def init_db():
    with app.app_context():
        db.create_all()
        
        admin_email = os.environ.get('ADMIN_EMAIL')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        admin_name = os.environ.get('ADMIN_NAME', 'Administrador')
        admin_phone = os.environ.get('ADMIN_PHONE')
        
        if not User.query.first():
            if admin_email and admin_password:
                admin = User(
                    name=admin_name,
                    email=admin_email,
                    role='ADMIN',
                    phone=admin_phone
                )
                admin.set_password(admin_password)
                print(f'Admin user created: {admin_email}')
            else:
                temp_password = os.urandom(8).hex()
                admin = User(
                    name='Admin Temporário',
                    email='admin@emunah.local',
                    role='ADMIN'
                )
                admin.set_password(temp_password)
                print('='*50)
                print('ATENÇÃO: Credenciais temporárias criadas!')
                print(f'Email: admin@emunah.local')
                print(f'Senha: {temp_password}')
                print('Configure ADMIN_EMAIL e ADMIN_PASSWORD nas variáveis de ambiente!')
                print('='*50)
            db.session.add(admin)
            
            # Sample suppliers
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
            
            # Sample prints
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
                name='Estampa Evangélica',
                description='Design com mensagem bíblica',
                colors=['Branco', 'Dourado'],
                positions=['Costas', 'Frente'],
                technique='dtf',
                dimensions='30x40cm',
                active=True
            )
            db.session.add(print1)
            db.session.add(print2)
            
            # Sample client
            client1 = Client(
                name='Igreja Nova Vida',
                cpf_cnpj='12.345.678/0001-90',
                email='contato@igrejanovavida.com',
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
