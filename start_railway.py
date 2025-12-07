#!/usr/bin/env python3
"""
Script de inicialização para Railway - versão otimizada.
"""

import os
import sys
import time

def fix_database_url():
    """Corrige a URL do banco de dados se necessário."""
    database_url = os.environ.get('DATABASE_URL', '')
    if database_url.startswith('postgres://'):
        os.environ['DATABASE_URL'] = database_url.replace('postgres://', 'postgresql://', 1)
        print("DATABASE_URL corrigida para formato postgresql://")

def init_database():
    """Inicializa o banco de dados de forma rápida."""
    print("Inicializando banco de dados...")
    
    try:
        from app import app, db, User
        
        with app.app_context():
            db.create_all()
            print("Tabelas criadas!")
            
            if not User.query.first():
                admin_email = os.environ.get('ADMIN_EMAIL', 'admin@emunah.local')
                admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
                admin_name = os.environ.get('ADMIN_NAME', 'Admin')
                
                admin = User(
                    name=admin_name,
                    email=admin_email,
                    role='ADMIN',
                    phone=os.environ.get('ADMIN_PHONE')
                )
                admin.set_password(admin_password)
                db.session.add(admin)
                db.session.commit()
                print(f"Admin criado: {admin_email}")
            
            print(f"Usuarios: {User.query.count()}")
        
        return True
    except Exception as e:
        print(f"Erro no banco: {e}")
        return False

def start_server():
    """Inicia o servidor Gunicorn."""
    port = os.environ.get('PORT', '8080')
    print(f"Iniciando servidor na porta {port}...")
    
    os.execvp('gunicorn', [
        'gunicorn',
        'app:app',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '2',
        '--timeout', '120',
        '--access-logfile', '-',
        '--error-logfile', '-'
    ])

if __name__ == '__main__':
    print("=" * 50)
    print("EMUNAH - Iniciando...")
    print("=" * 50)
    
    print(f"DATABASE_URL: {'OK' if os.environ.get('DATABASE_URL') else 'NAO CONFIGURADA'}")
    print(f"PORT: {os.environ.get('PORT', '8080')}")
    
    fix_database_url()
    init_database()
    start_server()
