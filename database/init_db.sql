-- =====================================================
-- EMUNAH - Script de Inicialização do Banco de Dados
-- Sistema de Vendas e Orçamentos para Camisetas
-- Para uso no Railway (PostgreSQL)
-- =====================================================

-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- TABELA: users (Usuários do sistema)
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'SELLER',
    phone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- =====================================================
-- TABELA: clients (Clientes)
-- =====================================================
CREATE TABLE IF NOT EXISTS clients (
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

CREATE INDEX IF NOT EXISTS idx_clients_name ON clients(name);
CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email);
CREATE INDEX IF NOT EXISTS idx_clients_cpf_cnpj ON clients(cpf_cnpj);

-- =====================================================
-- TABELA: suppliers (Fornecedores)
-- =====================================================
CREATE TABLE IF NOT EXISTS suppliers (
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

CREATE INDEX IF NOT EXISTS idx_suppliers_name ON suppliers(name);

-- =====================================================
-- TABELA: products (Produtos)
-- =====================================================
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    model VARCHAR(100) NOT NULL,
    fabric VARCHAR(100) NOT NULL,
    color VARCHAR(50) NOT NULL,
    sizes JSONB NOT NULL DEFAULT '[]'::jsonb,
    base_price NUMERIC(10, 2) DEFAULT 0,
    stock INTEGER DEFAULT 0,
    image_url VARCHAR(500),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_products_active ON products(active);

-- =====================================================
-- TABELA: prints (Estampas)
-- =====================================================
CREATE TABLE IF NOT EXISTS prints (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    file_url VARCHAR(500),
    colors JSONB NOT NULL DEFAULT '[]'::jsonb,
    positions JSONB NOT NULL DEFAULT '[]'::jsonb,
    technique VARCHAR(50) DEFAULT 'silk',
    dimensions VARCHAR(50),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_prints_name ON prints(name);
CREATE INDEX IF NOT EXISTS idx_prints_active ON prints(active);

-- =====================================================
-- TABELA: quotes (Cotações/Orçamentos)
-- =====================================================
CREATE TABLE IF NOT EXISTS quotes (
    id SERIAL PRIMARY KEY,
    quote_number VARCHAR(50) UNIQUE,
    
    -- Cliente (pode ser opcional para leads)
    client_id INTEGER REFERENCES clients(id) ON DELETE SET NULL,
    
    -- Informações de lead (quando não há cliente cadastrado)
    lead_name VARCHAR(255),
    lead_email VARCHAR(255),
    lead_phone VARCHAR(50),
    
    -- Relacionamentos
    seller_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    supplier_id INTEGER REFERENCES suppliers(id) ON DELETE SET NULL,
    product_id INTEGER REFERENCES products(id) ON DELETE SET NULL,
    print_id INTEGER REFERENCES prints(id) ON DELETE SET NULL,
    
    -- Detalhes do pedido
    items JSONB NOT NULL DEFAULT '[]'::jsonb,
    model VARCHAR(100),
    shirt_color VARCHAR(50),
    print_position VARCHAR(100),
    print_size VARCHAR(50),
    print_color VARCHAR(50),
    
    -- Preços
    total_quantity INTEGER DEFAULT 0,
    unit_price NUMERIC(10, 2),
    total_price NUMERIC(10, 2),
    down_payment_percent INTEGER DEFAULT 40,
    down_payment_value NUMERIC(10, 2),
    pix_key VARCHAR(100) DEFAULT '11998896725',
    
    -- Status: draft, pending, sent, approved, rejected, expired, converted
    status VARCHAR(50) DEFAULT 'draft',
    
    -- Entrega
    delivery_method VARCHAR(50) DEFAULT 'delivery',
    delivery_days INTEGER,
    delivery_date_estimated TIMESTAMP,
    
    -- Validade
    valid_until TIMESTAMP,
    
    -- Imagem e referência
    reference_url VARCHAR(500),
    image_path VARCHAR(500),
    
    -- Observações e timestamps
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP,
    approved_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_quotes_quote_number ON quotes(quote_number);
CREATE INDEX IF NOT EXISTS idx_quotes_status ON quotes(status);
CREATE INDEX IF NOT EXISTS idx_quotes_client_id ON quotes(client_id);
CREATE INDEX IF NOT EXISTS idx_quotes_seller_id ON quotes(seller_id);
CREATE INDEX IF NOT EXISTS idx_quotes_created_at ON quotes(created_at);

-- =====================================================
-- TABELA: orders (Pedidos)
-- =====================================================
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    quote_id INTEGER REFERENCES quotes(id) ON DELETE SET NULL,
    client_id INTEGER REFERENCES clients(id) ON DELETE SET NULL,
    supplier_id INTEGER REFERENCES suppliers(id) ON DELETE SET NULL,
    
    -- Informações de lead (copiadas da cotação)
    lead_name VARCHAR(255),
    lead_email VARCHAR(255),
    lead_phone VARCHAR(50),
    
    order_number VARCHAR(50) UNIQUE NOT NULL,
    
    -- Status: created, production, ready, shipping, delivered, cancelled
    status VARCHAR(50) DEFAULT 'created',
    
    -- Produção: cutting, printing, finishing, quality_check, ready
    production_step VARCHAR(50) DEFAULT 'cutting',
    progress INTEGER DEFAULT 0,
    
    -- Valores
    total_value NUMERIC(10, 2) NOT NULL,
    paid_value NUMERIC(10, 2) DEFAULT 0,
    
    -- Entrega
    delivery_method VARCHAR(50) DEFAULT 'delivery',
    delivery_date_estimated TIMESTAMP,
    delivery_date_actual TIMESTAMP,
    tracking_code VARCHAR(100),
    
    -- Referência
    reference_url VARCHAR(500),
    
    -- Observações e timestamps
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_orders_order_number ON orders(order_number);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_client_id ON orders(client_id);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);

-- =====================================================
-- TABELA: order_items (Itens do Pedido)
-- =====================================================
CREATE TABLE IF NOT EXISTS order_items (
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
    customization JSONB
);

CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);

-- =====================================================
-- TABELA: transactions (Transações/Pagamentos)
-- =====================================================
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    payment_method VARCHAR(50) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_transactions_order_id ON transactions(order_id);
CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status);

-- =====================================================
-- TABELA: email_logs (Log de Emails)
-- =====================================================
CREATE TABLE IF NOT EXISTS email_logs (
    id SERIAL PRIMARY KEY,
    recipient VARCHAR(255) NOT NULL,
    subject VARCHAR(500),
    email_type VARCHAR(50),
    status VARCHAR(50) DEFAULT 'sent',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_email_logs_recipient ON email_logs(recipient);
CREATE INDEX IF NOT EXISTS idx_email_logs_created_at ON email_logs(created_at);

-- =====================================================
-- COMENTÁRIOS NAS TABELAS
-- =====================================================
COMMENT ON TABLE users IS 'Usuários do sistema (admin, vendedores, fornecedores)';
COMMENT ON TABLE clients IS 'Clientes cadastrados no sistema';
COMMENT ON TABLE suppliers IS 'Fornecedores de camisetas e materiais';
COMMENT ON TABLE products IS 'Produtos disponíveis para venda';
COMMENT ON TABLE prints IS 'Estampas disponíveis para personalização';
COMMENT ON TABLE quotes IS 'Cotações/Orçamentos enviados aos clientes';
COMMENT ON TABLE orders IS 'Pedidos confirmados (convertidos de cotações)';
COMMENT ON TABLE order_items IS 'Itens individuais de cada pedido';
COMMENT ON TABLE transactions IS 'Transações financeiras (pagamentos)';
COMMENT ON TABLE email_logs IS 'Log de emails enviados pelo sistema';

-- =====================================================
-- FIM DO SCRIPT
-- =====================================================
