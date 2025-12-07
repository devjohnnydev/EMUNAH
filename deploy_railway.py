"""
Script de Deploy para Railway - Emunah Sistema
Este script configura todas as tabelas do banco de dados e popula dados iniciais
"""
import os
import sys

def check_environment():
    """Verifica se as variáveis de ambiente necessárias estão configuradas"""
    required_vars = ['DATABASE_URL']
    optional_vars = ['SECRET_KEY', 'SESSION_SECRET', 'ADMIN_EMAIL', 'ADMIN_PASSWORD']
    
    print("=" * 60)
    print("EMUNAH - Script de Deploy para Railway")
    print("=" * 60)
    print("\n[1/4] Verificando variáveis de ambiente...\n")
    
    missing = []
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"  ✓ {var}: configurado")
        else:
            print(f"  ✗ {var}: NÃO CONFIGURADO (obrigatório)")
            missing.append(var)
    
    print("\nVariáveis opcionais:")
    for var in optional_vars:
        value = os.environ.get(var)
        if value:
            print(f"  ✓ {var}: configurado")
        else:
            print(f"  - {var}: não configurado")
    
    if missing:
        print(f"\n✗ ERRO: Variáveis obrigatórias não configuradas: {', '.join(missing)}")
        print("Configure essas variáveis no painel do Railway antes do deploy.")
        return False
    
    return True


def create_tables():
    """Cria todas as tabelas do banco de dados"""
    print("\n[2/4] Criando tabelas do banco de dados...\n")
    
    try:
        from app import app, db
        
        with app.app_context():
            db.create_all()
            print("  ✓ Todas as tabelas criadas com sucesso!")
            
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"\n  Tabelas no banco de dados ({len(tables)}):")
            for table in sorted(tables):
                print(f"    - {table}")
        
        return True
    except Exception as e:
        print(f"  ✗ Erro ao criar tabelas: {e}")
        return False


def init_admin_user():
    """Inicializa o usuário administrador"""
    print("\n[3/4] Configurando usuário administrador...\n")
    
    try:
        from app import app, db, User
        
        with app.app_context():
            existing_users = User.query.count()
            
            if existing_users > 0:
                print(f"  ℹ Já existem {existing_users} usuário(s) no sistema.")
                admin = User.query.filter_by(role='ADMIN').first()
                if admin:
                    print(f"  ✓ Admin existente: {admin.email}")
            else:
                admin_email = os.environ.get('ADMIN_EMAIL')
                admin_password = os.environ.get('ADMIN_PASSWORD')
                admin_name = os.environ.get('ADMIN_NAME', 'Administrador')
                admin_phone = os.environ.get('ADMIN_PHONE')
                
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
                    print(f"  ✓ Usuário admin criado: {admin_email}")
                else:
                    print("  ⚠ ADMIN_EMAIL e ADMIN_PASSWORD não configurados.")
                    print("    Configure essas variáveis para criar o admin automaticamente.")
        
        return True
    except Exception as e:
        print(f"  ✗ Erro ao configurar admin: {e}")
        return False


def seed_initial_data():
    """Popula dados iniciais incluindo estampas evangélicas"""
    print("\n[4/4] Populando dados iniciais...\n")
    
    try:
        from app import app, db, Print, Supplier, Client
        
        with app.app_context():
            prints_count = Print.query.count()
            if prints_count < 30:
                print("  → Adicionando estampas evangélicas...")
                from seed_prints import ESTAMPAS_EMUNAH
                
                added = 0
                for estampa in ESTAMPAS_EMUNAH:
                    existing = Print.query.filter_by(name=estampa["name"]).first()
                    if not existing:
                        new_print = Print(
                            name=estampa["name"],
                            description=estampa["description"],
                            colors=estampa["colors"],
                            positions=estampa["positions"],
                            technique=estampa["technique"],
                            dimensions=estampa["dimensions"],
                            active=True
                        )
                        db.session.add(new_print)
                        added += 1
                
                if added > 0:
                    db.session.commit()
                    print(f"  ✓ {added} estampas evangélicas adicionadas!")
            else:
                print(f"  ✓ {prints_count} estampas já existem no banco.")
            
            suppliers_count = Supplier.query.count()
            if suppliers_count == 0:
                print("  → Adicionando fornecedores de exemplo...")
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
                db.session.commit()
                print("  ✓ Fornecedores de exemplo adicionados!")
            else:
                print(f"  ✓ {suppliers_count} fornecedor(es) já existe(m).")
            
            clients_count = Client.query.count()
            if clients_count == 0:
                print("  → Adicionando cliente de exemplo...")
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
                print("  ✓ Cliente de exemplo adicionado!")
            else:
                print(f"  ✓ {clients_count} cliente(s) já existe(m).")
        
        return True
    except Exception as e:
        print(f"  ✗ Erro ao popular dados: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Executa o script de deploy completo"""
    print("\n")
    
    if not check_environment():
        sys.exit(1)
    
    if not create_tables():
        sys.exit(1)
    
    if not init_admin_user():
        print("  ⚠ Continuando sem configurar admin...")
    
    if not seed_initial_data():
        print("  ⚠ Continuando sem dados iniciais...")
    
    print("\n" + "=" * 60)
    print("DEPLOY CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    print("\nPróximos passos:")
    print("  1. Acesse a URL do seu projeto Railway")
    print("  2. Faça login com as credenciais de admin")
    print("  3. Configure os dados da sua empresa em Configurações")
    print("\nSuporte: Entre em contato com o desenvolvedor")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
