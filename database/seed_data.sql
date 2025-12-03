-- =====================================================
-- EMUNAH - Script de Dados de Exemplo
-- Execute após o init_db.sql
-- =====================================================

-- =====================================================
-- FORNECEDORES DE EXEMPLO
-- =====================================================
INSERT INTO suppliers (name, contact_name, email, phone, production_time_days, rating, payment_method, notes) 
VALUES 
    ('Gráfica Express', 'Carlos Silva', 'contato@graficaexpress.com', '(11) 99999-1111', 7, 4.5, 'PIX, Boleto', 'Fornecedor principal de silk screen'),
    ('Estamparia Premium', 'Maria Santos', 'comercial@estampariapremium.com', '(11) 99999-2222', 5, 5.0, 'PIX, Cartão', 'Especialista em sublimação'),
    ('Malhas Brasil', 'João Oliveira', 'vendas@malhasbrasil.com', '(11) 99999-3333', 3, 4.0, 'Boleto, Transferência', 'Fornecedor de malhas em atacado')
ON CONFLICT DO NOTHING;

-- =====================================================
-- ESTAMPAS DE EXEMPLO
-- =====================================================
INSERT INTO prints (name, description, colors, positions, technique, dimensions, active)
VALUES 
    ('Versículo Salmos 23', 'Estampa com versículo bíblico Salmos 23:1 - O Senhor é meu pastor', '["Preto", "Branco", "Dourado"]', '["Frente", "Costas"]', 'silk', 'A4', true),
    ('Cruz Minimalista', 'Design de cruz em estilo minimalista moderno', '["Preto", "Branco"]', '["Frente"]', 'sublimacao', '15x20cm', true),
    ('Fé Caligráfica', 'Palavra FÉ em caligrafia artística elegante', '["Preto", "Dourado", "Prata"]', '["Frente", "Manga"]', 'silk', '20x15cm', true),
    ('Leão de Judá', 'Ilustração do Leão de Judá com coroa', '["Preto", "Dourado", "Vermelho"]', '["Frente", "Costas"]', 'dtf', 'A3', true),
    ('Filipenses 4:13', 'Versículo "Tudo posso naquele que me fortalece"', '["Preto", "Branco", "Azul"]', '["Frente"]', 'silk', '25x15cm', true)
ON CONFLICT DO NOTHING;

-- =====================================================
-- PRODUTOS DE EXEMPLO
-- =====================================================
INSERT INTO products (name, model, fabric, color, sizes, base_price, stock, active)
VALUES 
    ('Camiseta Básica', 'Tradicional', 'Algodão 100%', 'Branco', '{"P": 10, "M": 15, "G": 12, "GG": 8}', 29.90, 45, true),
    ('Camiseta Básica', 'Tradicional', 'Algodão 100%', 'Preto', '{"P": 8, "M": 12, "G": 10, "GG": 6}', 29.90, 36, true),
    ('Camiseta Premium', 'Slim Fit', 'Algodão Penteado', 'Branco', '{"P": 5, "M": 8, "G": 7, "GG": 4}', 39.90, 24, true),
    ('Camiseta Premium', 'Slim Fit', 'Algodão Penteado', 'Preto', '{"P": 6, "M": 10, "G": 8, "GG": 5}', 39.90, 29, true),
    ('Baby Look', 'Feminino', 'Algodão', 'Branco', '{"PP": 5, "P": 8, "M": 10, "G": 6}', 34.90, 29, true),
    ('Regata', 'Tradicional', 'Malha Fria', 'Branco', '{"P": 6, "M": 8, "G": 7, "GG": 4}', 24.90, 25, true)
ON CONFLICT DO NOTHING;

-- =====================================================
-- CLIENTES DE EXEMPLO
-- =====================================================
INSERT INTO clients (name, cpf_cnpj, email, phone, address, city, state, zip_code)
VALUES 
    ('Igreja Batista Central', '12.345.678/0001-90', 'contato@ibcentral.com', '(11) 99999-3333', 'Rua da Paz, 100', 'São Paulo', 'SP', '01310-100'),
    ('Ministério de Jovens Renovar', '23.456.789/0001-01', 'jovens@renovar.org', '(11) 99999-4444', 'Av. da Esperança, 200', 'São Paulo', 'SP', '04567-000'),
    ('Comunidade Vida Nova', '34.567.890/0001-12', 'eventos@vidanova.org', '(11) 99999-5555', 'Rua do Amor, 300', 'Campinas', 'SP', '13010-020'),
    ('Pastor João Silva', '123.456.789-00', 'pastor.joao@email.com', '(11) 99999-6666', 'Rua Bíblica, 50', 'São Paulo', 'SP', '01234-567'),
    ('Maria Evangelista', '234.567.890-11', 'maria.eva@email.com', '(11) 99999-7777', 'Av. da Fé, 150', 'Guarulhos', 'SP', '07000-000')
ON CONFLICT DO NOTHING;

-- =====================================================
-- FIM DO SCRIPT DE DADOS
-- =====================================================
