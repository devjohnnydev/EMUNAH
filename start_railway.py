#!/usr/bin/env python3
"""
Script de inicialização robusto para Railway.
Aguarda o banco de dados estar disponível e inicializa a aplicação.
"""

import os
import sys
import time
import subprocess

def wait_for_database(max_retries=30, delay=2):
    """Aguarda o banco de dados PostgreSQL estar disponível."""
    
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("AVISO: DATABASE_URL não configurada. Usando SQLite local.")
        return True
    
    print(f"Aguardando conexão com o banco de dados...")
    
    # Corrigir URL do Postgres se necessário
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
        os.environ['DATABASE_URL'] = database_url
    
    import psycopg2
    from urllib.parse import urlparse
    
    parsed = urlparse(database_url)
    
    for attempt in range(1, max_retries + 1):
        try:
            conn = psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port or 5432,
                user=parsed.username,
                password=parsed.password,
                dbname=parsed.path[1:],
                connect_timeout=5
            )
            conn.close()
            print(f"Banco de dados conectado! (tentativa {attempt})")
            return True
        except Exception as e:
            print(f"Tentativa {attempt}/{max_retries}: Aguardando banco... ({str(e)[:50]})")
            time.sleep(delay)
    
    print("ERRO: Não foi possível conectar ao banco de dados após várias tentativas.")
    return False


def init_database():
    """Inicializa o banco de dados."""
    print("\n" + "=" * 60)
    print("Inicializando banco de dados...")
    print("=" * 60)
    
    try:
        # Importar e inicializar o banco
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app import app, db, User
        
        with app.app_context():
            # Criar tabelas
            db.create_all()
            print("Tabelas criadas com sucesso!")
            
            # Criar admin se não existir
            if not User.query.first():
                admin_email = os.environ.get('ADMIN_EMAIL', 'admin@emunah.local')
                admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
                admin_name = os.environ.get('ADMIN_NAME', 'Administrador')
                admin_phone = os.environ.get('ADMIN_PHONE')
                
                admin = User(
                    name=admin_name,
                    email=admin_email,
                    role='ADMIN',
                    phone=admin_phone
                )
                admin.set_password(admin_password)
                db.session.add(admin)
                db.session.commit()
                print(f"Admin criado: {admin_email}")
            else:
                print("Admin já existe.")
            
            # Contar registros
            users_count = User.query.count()
            print(f"Total de usuários: {users_count}")
        
        print("Banco de dados inicializado com sucesso!")
        return True
        
    except Exception as e:
        print(f"ERRO ao inicializar banco: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def start_gunicorn():
    """Inicia o servidor Gunicorn."""
    port = os.environ.get('PORT', '8080')
    
    print("\n" + "=" * 60)
    print(f"Iniciando Gunicorn na porta {port}...")
    print("=" * 60)
    
    cmd = [
        'gunicorn',
        'app:app',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '2',
        '--timeout', '120',
        '--access-logfile', '-',
        '--error-logfile', '-',
        '--capture-output',
        '--enable-stdio-inheritance'
    ]
    
    # Substituir o processo atual pelo gunicorn
    os.execvp('gunicorn', cmd)


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("EMUNAH - Iniciando Aplicação no Railway")
    print("=" * 60)
    
    # Verificar variáveis de ambiente importantes
    print("\nVariáveis de ambiente:")
    print(f"  DATABASE_URL: {'Configurada' if os.environ.get('DATABASE_URL') else 'NÃO CONFIGURADA'}")
    print(f"  PORT: {os.environ.get('PORT', '8080 (padrão)')}")
    print(f"  ADMIN_EMAIL: {os.environ.get('ADMIN_EMAIL', 'NÃO CONFIGURADA')}")
    
    # Aguardar banco de dados
    if not wait_for_database():
        print("Continuando sem verificação do banco...")
    
    # Inicializar banco
    if not init_database():
        print("AVISO: Falha na inicialização do banco, mas tentando iniciar o servidor...")
    
    # Iniciar servidor
    start_gunicorn()
