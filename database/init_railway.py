#!/usr/bin/env python3
"""
EMUNAH - Script de Inicialização do Banco de Dados para Railway
Este script inicializa o banco de dados PostgreSQL no Railway.

Uso:
    python database/init_railway.py

Variáveis de ambiente necessárias:
    - DATABASE_URL: URL de conexão com o PostgreSQL
    - ADMIN_EMAIL: Email do administrador
    - ADMIN_PASSWORD: Senha do administrador
    - ADMIN_NAME (opcional): Nome do administrador
    - ADMIN_PHONE (opcional): Telefone do administrador
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, User, Client, Supplier, Product, Print


def init_database():
    """Inicializa o banco de dados com as tabelas e dados iniciais."""
    
    with app.app_context():
        print("=" * 60)
        print("EMUNAH - Inicialização do Banco de Dados")
        print("=" * 60)
        
        print("\n[1/4] Criando tabelas do banco de dados...")
        db.create_all()
        print("      Tabelas criadas com sucesso!")
        
        print("\n[2/4] Verificando usuário administrador...")
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
                db.session.add(admin)
                db.session.commit()
                print(f"      Admin criado: {admin_email}")
            else:
                temp_password = os.urandom(8).hex()
                admin = User(
                    name='Admin Temporário',
                    email='admin@emunah.local',
                    role='ADMIN'
                )
                admin.set_password(temp_password)
                db.session.add(admin)
                db.session.commit()
                print("\n      ATENÇÃO: Credenciais temporárias criadas!")
                print(f"      Email: admin@emunah.local")
                print(f"      Senha: {temp_password}")
                print("      Configure ADMIN_EMAIL e ADMIN_PASSWORD nas variáveis de ambiente.")
        else:
            print("      Usuário administrador já existe.")
        
        print("\n[3/4] Inserindo dados de exemplo...")
        create_sample_data()
        
        print("\n[4/4] Verificação final...")
        verify_database()
        
        print("\n" + "=" * 60)
        print("Banco de dados inicializado com sucesso!")
        print("=" * 60)


def create_sample_data():
    """Cria dados de exemplo se não existirem."""
    
    if not Supplier.query.first():
        suppliers = [
            Supplier(
                name='Gráfica Express',
                contact_name='Carlos Silva',
                email='contato@graficaexpress.com',
                phone='(11) 99999-1111',
                production_time_days=7,
                rating=4.5,
                payment_method='PIX, Boleto'
            ),
            Supplier(
                name='Estamparia Premium',
                contact_name='Maria Santos',
                email='comercial@estampariapremium.com',
                phone='(11) 99999-2222',
                production_time_days=5,
                rating=5.0,
                payment_method='PIX, Cartão'
            )
        ]
        db.session.add_all(suppliers)
        db.session.commit()
        print("      Fornecedores de exemplo criados.")
    
    if not Print.query.first():
        prints = [
            Print(
                name='Versículo Salmos 23',
                description='Estampa com versículo bíblico Salmos 23:1',
                colors=['Preto', 'Branco', 'Dourado'],
                positions=['Frente', 'Costas'],
                technique='silk',
                dimensions='A4'
            ),
            Print(
                name='Cruz Minimalista',
                description='Design de cruz em estilo minimalista',
                colors=['Preto', 'Branco'],
                positions=['Frente'],
                technique='sublimacao',
                dimensions='15x20cm'
            ),
            Print(
                name='Fé Caligráfica',
                description='Palavra FÉ em caligrafia artística',
                colors=['Preto', 'Dourado', 'Prata'],
                positions=['Frente', 'Manga'],
                technique='silk',
                dimensions='20x15cm'
            )
        ]
        db.session.add_all(prints)
        db.session.commit()
        print("      Estampas de exemplo criadas.")
    
    if not Client.query.first():
        clients = [
            Client(
                name='Igreja Batista Central',
                email='contato@ibcentral.com',
                phone='(11) 99999-3333',
                city='São Paulo',
                state='SP'
            ),
            Client(
                name='Ministério de Jovens Renovar',
                email='jovens@renovar.org',
                phone='(11) 99999-4444',
                city='São Paulo',
                state='SP'
            )
        ]
        db.session.add_all(clients)
        db.session.commit()
        print("      Clientes de exemplo criados.")


def verify_database():
    """Verifica se o banco de dados foi inicializado corretamente."""
    
    users_count = User.query.count()
    clients_count = Client.query.count()
    suppliers_count = Supplier.query.count()
    prints_count = Print.query.count()
    
    print(f"      Usuários: {users_count}")
    print(f"      Clientes: {clients_count}")
    print(f"      Fornecedores: {suppliers_count}")
    print(f"      Estampas: {prints_count}")


if __name__ == '__main__':
    init_database()
