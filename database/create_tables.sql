-- Emunah Database Schema
-- Complete SQL script for creating all tables
-- PostgreSQL compatible

-- Drop existing tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS email_logs CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS quotes CASCADE;
DROP TABLE IF EXISTS prints CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS clients CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'SELLER',
    phone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Clients table
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cpf_cnpj VARCHAR(20),
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Suppliers table
CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255),
    cnpj VARCHAR(20),
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    production_time_days INTEGER DEFAULT 7,
    rating NUMERIC(2, 1) DEFAULT 0,
    payment_method VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    model VARCHAR(100) NOT NULL,
    fabric VARCHAR(100) NOT NULL,
    color VARCHAR(50) NOT NULL,
    sizes JSON NOT NULL,
    base_price NUMERIC(10, 2) DEFAULT 0,
    stock INTEGER DEFAULT 0,
    image_url VARCHAR(500),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Prints (Estampas) table
CREATE TABLE prints (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    file_url VARCHAR(500),
    colors JSON NOT NULL,
    positions JSON NOT NULL,
    technique VARCHAR(50) DEFAULT 'silk',
    dimensions VARCHAR(50),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quotes (Cotacoes) table
CREATE TABLE quotes (
    id SERIAL PRIMARY KEY,
    quote_number VARCHAR(50) UNIQUE,
    client_id INTEGER REFERENCES clients(id) ON DELETE SET NULL,
    lead_name VARCHAR(255),
    lead_email VARCHAR(255),
    lead_phone VARCHAR(50),
    seller_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    supplier_id INTEGER REFERENCES suppliers(id) ON DELETE SET NULL,
    product_id INTEGER REFERENCES products(id) ON DELETE SET NULL,
    print_id INTEGER REFERENCES prints(id) ON DELETE SET NULL,
    items JSON NOT NULL DEFAULT '[]',
    model VARCHAR(100),
    shirt_color VARCHAR(50),
    print_position VARCHAR(100),
    print_size VARCHAR(50),
    print_color VARCHAR(50),
    total_quantity INTEGER DEFAULT 0,
    unit_price NUMERIC(10, 2),
    total_price NUMERIC(10, 2),
    down_payment_percent INTEGER DEFAULT 40,
    down_payment_value NUMERIC(10, 2),
    pix_key VARCHAR(100) DEFAULT '11998896725',
    status VARCHAR(50) DEFAULT 'draft',
    delivery_method VARCHAR(50) DEFAULT 'delivery',
    delivery_days INTEGER,
    delivery_date_estimated TIMESTAMP,
    valid_until TIMESTAMP,
    reference_url VARCHAR(500),
    image_path VARCHAR(500),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP,
    approved_at TIMESTAMP
);

-- Orders (Pedidos) table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    quote_id INTEGER REFERENCES quotes(id) ON DELETE SET NULL,
    client_id INTEGER REFERENCES clients(id) ON DELETE SET NULL,
    supplier_id INTEGER REFERENCES suppliers(id) ON DELETE SET NULL,
    lead_name VARCHAR(255),
    lead_email VARCHAR(255),
    lead_phone VARCHAR(50),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'created',
    production_step VARCHAR(50) DEFAULT 'cutting',
    progress INTEGER DEFAULT 0,
    total_value NUMERIC(10, 2) NOT NULL,
    paid_value NUMERIC(10, 2) DEFAULT 0,
    delivery_method VARCHAR(50) DEFAULT 'delivery',
    delivery_date_estimated TIMESTAMP,
    delivery_date_actual TIMESTAMP,
    tracking_code VARCHAR(100),
    reference_url VARCHAR(500),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMP
);

-- Order Items table
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE SET NULL,
    print_id INTEGER REFERENCES prints(id) ON DELETE SET NULL,
    description VARCHAR(500),
    size VARCHAR(20),
    color VARCHAR(50),
    quantity INTEGER DEFAULT 1,
    unit_price NUMERIC(10, 2),
    total_price NUMERIC(10, 2),
    customization JSON
);

-- Transactions (Pagamentos) table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    payment_method VARCHAR(50) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

-- Email Logs table
CREATE TABLE email_logs (
    id SERIAL PRIMARY KEY,
    recipient VARCHAR(255) NOT NULL,
    subject VARCHAR(500),
    email_type VARCHAR(50),
    status VARCHAR(50) DEFAULT 'sent',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_quotes_client_id ON quotes(client_id);
CREATE INDEX idx_quotes_seller_id ON quotes(seller_id);
CREATE INDEX idx_quotes_status ON quotes(status);
CREATE INDEX idx_quotes_created_at ON quotes(created_at);

CREATE INDEX idx_orders_client_id ON orders(client_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);

CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_transactions_order_id ON transactions(order_id);

CREATE INDEX idx_clients_name ON clients(name);
CREATE INDEX idx_clients_email ON clients(email);

CREATE INDEX idx_products_active ON products(active);
CREATE INDEX idx_prints_active ON prints(active);

CREATE INDEX idx_users_email ON users(email);

-- Comments for documentation
COMMENT ON TABLE users IS 'System users (admins, sellers)';
COMMENT ON TABLE clients IS 'Customer information';
COMMENT ON TABLE suppliers IS 'Fabric and production suppliers';
COMMENT ON TABLE products IS 'Product catalog (shirts, etc)';
COMMENT ON TABLE prints IS 'Print designs and specifications';
COMMENT ON TABLE quotes IS 'Price quotations for customers';
COMMENT ON TABLE orders IS 'Confirmed orders from quotes';
COMMENT ON TABLE order_items IS 'Individual items within an order';
COMMENT ON TABLE transactions IS 'Payment transactions for orders';
COMMENT ON TABLE email_logs IS 'Email sending history and logs';
