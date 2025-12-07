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
    
    prints_count = Print.query.count()
    if prints_count < 30:
        ESTAMPAS_EMUNAH = [
            {"name": "Emunah - Fé que Move", "description": "Estampa com a palavra Emunah em destaque e versículo 'A fé é a certeza daquilo que esperamos' (Hb 11:1)", "colors": ["Branco", "Dourado"], "positions": ["Peito", "Costas"], "technique": "silk", "dimensions": "25x30cm"},
            {"name": "Emunah - Cruz Minimalista", "description": "Cruz estilizada com o logo Emunah e frase 'Vista-se com propósito'", "colors": ["Branco", "Borgonha"], "positions": ["Peito", "Manga"], "technique": "silk", "dimensions": "15x20cm"},
            {"name": "Emunah - Salmo 23", "description": "Design elegante com 'O Senhor é meu pastor, nada me faltará' e símbolo de ovelha", "colors": ["Branco", "Areia"], "positions": ["Costas"], "technique": "dtf", "dimensions": "30x40cm"},
            {"name": "Emunah - Leão de Judá", "description": "Leão majestoso com coroa e texto 'Emunah - Força na Fé'", "colors": ["Dourado", "Preto", "Branco"], "positions": ["Costas", "Peito"], "technique": "dtf", "dimensions": "35x40cm"},
            {"name": "Emunah - Filipenses 4:13", "description": "Estampa tipográfica 'Tudo posso naquele que me fortalece' com logo Emunah", "colors": ["Branco"], "positions": ["Peito", "Costas"], "technique": "silk", "dimensions": "20x25cm"},
            {"name": "Emunah - Pomba da Paz", "description": "Pomba em voo com ramo de oliveira e texto 'Paz que excede todo entendimento'", "colors": ["Branco", "Dourado", "Verde"], "positions": ["Costas"], "technique": "dtf", "dimensions": "28x35cm"},
            {"name": "Emunah - Coroa da Vida", "description": "Coroa delicada com flores e versículo 'Sê fiel até a morte' (Ap 2:10)", "colors": ["Dourado", "Rosa", "Branco"], "positions": ["Peito"], "technique": "dtf", "dimensions": "18x20cm"},
            {"name": "Emunah - Âncora da Alma", "description": "Âncora estilizada com 'Esperança segura e firme para a alma' (Hb 6:19)", "colors": ["Azul Marinho", "Branco", "Dourado"], "positions": ["Costas", "Peito"], "technique": "silk", "dimensions": "25x30cm"},
            {"name": "Emunah - Isaías 41:10", "description": "Design floral com 'Não temas, porque eu sou contigo' e logo Emunah", "colors": ["Branco", "Rosa", "Verde"], "positions": ["Costas"], "technique": "dtf", "dimensions": "30x35cm"},
            {"name": "Emunah - Peixe Cristão", "description": "Símbolo Ichthys moderno com 'Emunah - Seguidor de Cristo'", "colors": ["Branco", "Azul"], "positions": ["Peito", "Manga"], "technique": "silk", "dimensions": "12x8cm"},
            {"name": "Emunah - Montanhas da Fé", "description": "Montanhas geométricas com 'A fé move montanhas' (Mt 17:20)", "colors": ["Cinza", "Branco", "Dourado"], "positions": ["Costas"], "technique": "dtf", "dimensions": "30x25cm"},
            {"name": "Emunah - Coração Adorador", "description": "Coração com notas musicais e 'Feito para adorar' - logo Emunah", "colors": ["Vermelho", "Branco", "Preto"], "positions": ["Peito"], "technique": "silk", "dimensions": "18x20cm"},
            {"name": "Emunah - Provérbios 31", "description": "Design feminino elegante com 'Mulher virtuosa, quem a achará?' e coroa", "colors": ["Rosa", "Dourado", "Branco"], "positions": ["Costas"], "technique": "dtf", "dimensions": "28x35cm"},
            {"name": "Emunah - Josué 1:9", "description": "Estampa masculina 'Seja forte e corajoso' com escudo e espada", "colors": ["Preto", "Dourado", "Branco"], "positions": ["Costas"], "technique": "dtf", "dimensions": "30x40cm"},
            {"name": "Emunah - Luz do Mundo", "description": "Lâmpada/vela com raios de luz e 'Vós sois a luz do mundo' (Mt 5:14)", "colors": ["Amarelo", "Branco", "Laranja"], "positions": ["Peito", "Costas"], "technique": "silk", "dimensions": "22x25cm"},
            {"name": "Emunah - Oliveira Sagrada", "description": "Ramo de oliveira estilizado com 'Plantados na casa do Senhor' (Sl 92:13)", "colors": ["Verde", "Marrom", "Branco"], "positions": ["Costas"], "technique": "dtf", "dimensions": "25x30cm"},
            {"name": "Emunah - Mãos em Oração", "description": "Mãos em oração com rosário e 'Orai sem cessar' (1Ts 5:17)", "colors": ["Branco", "Dourado"], "positions": ["Costas", "Peito"], "technique": "silk", "dimensions": "20x28cm"},
            {"name": "Emunah - Cordeiro de Deus", "description": "Cordeiro com auréola e bandeira, 'Eis o Cordeiro de Deus' (Jo 1:29)", "colors": ["Branco", "Dourado", "Vermelho"], "positions": ["Costas"], "technique": "dtf", "dimensions": "30x35cm"},
            {"name": "Emunah - Água Viva", "description": "Ondas de água com 'Quem beber da água que eu lhe der nunca terá sede' (Jo 4:14)", "colors": ["Azul", "Branco", "Ciano"], "positions": ["Costas"], "technique": "dtf", "dimensions": "28x32cm"},
            {"name": "Emunah - Videira Verdadeira", "description": "Ramos de videira com uvas e 'Eu sou a videira, vós os ramos' (Jo 15:5)", "colors": ["Verde", "Roxo", "Marrom"], "positions": ["Costas"], "technique": "dtf", "dimensions": "30x35cm"},
            {"name": "Emunah - Armadura de Deus", "description": "Elementos da armadura espiritual com 'Revesti-vos de toda armadura' (Ef 6:11)", "colors": ["Dourado", "Prata", "Branco"], "positions": ["Costas"], "technique": "dtf", "dimensions": "35x45cm"},
            {"name": "Emunah - Sal da Terra", "description": "Cristal de sal estilizado com 'Vós sois o sal da terra' (Mt 5:13)", "colors": ["Branco", "Cinza", "Dourado"], "positions": ["Peito"], "technique": "silk", "dimensions": "15x18cm"},
            {"name": "Emunah - Bom Pastor", "description": "Cajado pastoral com ovelhas e 'O bom pastor dá a vida pelas ovelhas' (Jo 10:11)", "colors": ["Marrom", "Branco", "Verde"], "positions": ["Costas"], "technique": "dtf", "dimensions": "28x35cm"},
            {"name": "Emunah - Estrela de Davi", "description": "Estrela de seis pontas moderna com 'Emunah - Herança de Fé'", "colors": ["Dourado", "Branco"], "positions": ["Peito", "Manga"], "technique": "silk", "dimensions": "12x12cm"},
            {"name": "Emunah - Pão da Vida", "description": "Trigo e pão com 'Eu sou o pão da vida' (Jo 6:35) e cálice", "colors": ["Dourado", "Marrom", "Branco"], "positions": ["Costas"], "technique": "dtf", "dimensions": "25x30cm"},
            {"name": "Emunah - Ressurreição", "description": "Túmulo vazio com sol nascente e 'Ele ressuscitou!' (Mt 28:6)", "colors": ["Laranja", "Amarelo", "Branco"], "positions": ["Costas"], "technique": "dtf", "dimensions": "30x35cm"},
            {"name": "Emunah - Fruto do Espírito", "description": "Árvore com 9 frutos representando Gálatas 5:22-23 e logo Emunah", "colors": ["Verde", "Colorido", "Marrom"], "positions": ["Costas"], "technique": "dtf", "dimensions": "32x40cm"},
            {"name": "Emunah - Apocalipse 22:13", "description": "Alfa e Ômega estilizados com 'Eu sou o Alfa e o Ômega'", "colors": ["Dourado", "Branco", "Preto"], "positions": ["Costas", "Peito"], "technique": "silk", "dimensions": "25x28cm"},
            {"name": "Emunah - Caminho da Vida", "description": "Estrada/caminho com cruz ao fundo e 'Eu sou o caminho, a verdade e a vida' (Jo 14:6)", "colors": ["Marrom", "Azul", "Branco"], "positions": ["Costas"], "technique": "dtf", "dimensions": "30x40cm"},
            {"name": "Emunah - Graça Infinita", "description": "Design caligráfico elegante com 'Pela graça sois salvos' (Ef 2:8) e símbolo infinito", "colors": ["Branco", "Dourado"], "positions": ["Peito", "Costas"], "technique": "silk", "dimensions": "22x15cm"}
        ]
        
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
            print(f"      {added} estampas evangélicas Emunah adicionadas.")
        else:
            print("      Estampas já existem no banco.")
    else:
        print(f"      {prints_count} estampas já cadastradas.")
    
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
