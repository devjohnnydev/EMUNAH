#!/bin/bash
# EMUNAH - Railway Deployment Script
# Este script prepara o ambiente e executa o deploy completo

echo "================================================"
echo "EMUNAH - Sistema de Vendas e Orçamentos"
echo "Railway Deployment Script v2.0"
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    exit 1
fi

# Install dependencies
echo ""
echo "[1/3] Instalando dependências Python..."
pip install -r requirements.txt --quiet

# Run the complete deploy script
echo ""
echo "[2/3] Executando script de deploy..."
python3 deploy_railway.py

# Seed prints if needed
echo ""
echo "[3/3] Verificando estampas evangélicas..."
python3 seed_prints.py

echo ""
echo "================================================"
echo "DEPLOY CONCLUÍDO!"
echo "================================================"
echo ""
echo "Variáveis de ambiente necessárias no Railway:"
echo ""
echo "OBRIGATÓRIAS:"
echo "  - DATABASE_URL (PostgreSQL - adicionado automaticamente)"
echo "  - SECRET_KEY ou SESSION_SECRET (segurança de sessão)"
echo ""
echo "ADMIN (recomendadas):"
echo "  - ADMIN_EMAIL (email do administrador)"
echo "  - ADMIN_PASSWORD (senha do administrador)"
echo "  - ADMIN_NAME (nome do administrador)"
echo "  - ADMIN_PHONE (telefone do administrador)"
echo ""
echo "EMAIL (opcionais):"
echo "  - MAIL_SERVER (servidor SMTP, padrão: smtp.gmail.com)"
echo "  - MAIL_PORT (porta SMTP, padrão: 587)"
echo "  - MAIL_USERNAME (usuário SMTP)"
echo "  - MAIL_PASSWORD (senha SMTP ou app password)"
echo "  - MAIL_DEFAULT_SENDER (email remetente)"
echo ""
echo "================================================"
