#!/usr/bin/env python3
"""
Emunah - Sistema de Vendas e Orçamentos
Script de inicialização para desenvolvimento local
"""
from app import app, init_db

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
