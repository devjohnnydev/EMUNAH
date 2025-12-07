# EMUNAH - Sistema de Vendas e Orçamentos

## Visão Geral

EMUNAH é um sistema web completo para gerenciamento de vendas e produção de camisetas personalizadas evangélicas. O sistema permite criar cotações (com ou sem clientes cadastrados), acompanhar pedidos, gerenciar fornecedores, produtos e estampas, com controle de acesso baseado em funções.

**Funcionalidades Principais:**
- Cotações flexíveis (com cliente cadastrado ou lead/prospect)
- Conversão automática de cotação aprovada para pedido
- Acompanhamento de produção e entrega
- Dashboard com métricas de vendas
- Gestão de fornecedores, produtos e estampas
- Controle financeiro de pagamentos

## Credenciais do Administrador

As credenciais são configuradas via variáveis de ambiente:
- `ADMIN_EMAIL` - Email do administrador
- `ADMIN_PASSWORD` - Senha do administrador
- `ADMIN_NAME` - Nome do administrador
- `ADMIN_PHONE` - Telefone do administrador

## Arquitetura do Sistema

### Stack Tecnológica

**Backend:**
- Python 3.x com Flask
- SQLAlchemy ORM
- Flask-Login para autenticação
- Flask-Migrate para migrações de banco
- Gunicorn como servidor WSGI

**Frontend:**
- HTML5/CSS3 com Jinja2 templates
- Tailwind CSS (via CDN em desenvolvimento)
- Chart.js para gráficos do dashboard
- Design responsivo

**Banco de Dados:**
- PostgreSQL (Replit e Railway/Neon)

### Estrutura de Arquivos

```
├── app.py           # Aplicação Flask, modelos e rotas
├── main.py          # Ponto de entrada para Gunicorn
├── templates/       # Templates Jinja2
│   ├── base.html    # Template base com menu lateral
│   ├── login.html   # Página de login
│   ├── dashboard.html
│   ├── quotes.html, quote_form.html, quote_view.html
│   ├── orders.html, order_form.html, order_view.html
│   ├── clients.html, client_form.html
│   ├── suppliers.html, supplier_form.html
│   ├── products.html, product_form.html
│   ├── prints.html, print_form.html
│   ├── budgets.html, budget_form.html
│   └── transactions.html
├── static/
│   ├── images/      # Logos EMUNAH (logo_emunah.png, logo_fundo_bege.png)
│   └── uploads/
│       ├── quotes/  # Imagens de referência das cotações
│       └── prints/  # Imagens das estampas (upload local)
├── database/        # Scripts de banco de dados
│   ├── init_db.sql      # Script SQL para criar tabelas
│   ├── seed_data.sql    # Dados de exemplo
│   ├── init_railway.py  # Script Python para Railway
│   └── README.md        # Documentação
├── requirements.txt # Dependências Python
├── nixpacks.toml    # Configuração Nixpacks (Railway)
├── railway.json     # Configuração Railway
└── Procfile         # Comando de inicialização
```

### Modelos de Dados

- **User**: Usuários com papéis (ADMIN, SELLER, SUPPLIER)
- **Client**: Clientes cadastrados
- **Supplier**: Fornecedores com avaliação e tempo de produção
- **Product**: Produtos com tamanhos, cores e preços
- **Print**: Estampas com posições, técnicas e cores
- **Quote**: Cotações (podem usar lead ou cliente cadastrado)
- **Order**: Pedidos gerados de cotações aprovadas
- **Budget**: Orçamentos formais
- **Transaction**: Pagamentos vinculados a pedidos

### Fluxo de Trabalho

1. **Cotação** → Vendedor cria cotação para cliente ou lead
2. **Aprovação** → Cliente aprova cotação
3. **Pedido** → Sistema cria pedido automaticamente
4. **Produção** → Acompanhamento por etapas (Corte → Estampa → Acabamento → Qualidade)
5. **Entrega** → Envio ou retirada com rastreamento
6. **Pagamento** → Registro de transações

## Variáveis de Ambiente

**Obrigatórias:**
- `DATABASE_URL` - String de conexão PostgreSQL
- `SECRET_KEY` ou `SESSION_SECRET` - Chave secreta para sessões

**Administrador (primeira execução):**
- `ADMIN_EMAIL` - Email do admin
- `ADMIN_PASSWORD` - Senha do admin
- `ADMIN_NAME` - Nome do admin
- `ADMIN_PHONE` - Telefone do admin

**Email (opcional):**
- `MAIL_SERVER` - Servidor SMTP (padrão: smtp.gmail.com)
- `MAIL_PORT` - Porta SMTP (padrão: 587)
- `MAIL_USERNAME` - Usuário SMTP
- `MAIL_PASSWORD` - Senha SMTP
- `MAIL_DEFAULT_SENDER` - Email remetente

## Deployment

### Railway

1. Configure as variáveis de ambiente no Railway
2. Conecte o repositório
3. Deploy automático via `railway.json`

O arquivo `railway.json` configura:
- Build com Nixpacks
- Inicialização do banco + Gunicorn
- Health check em `/login`
- Restart automático em falhas

### Replit

O workflow `Start application` executa:
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## Preferências do Usuário

- Linguagem: Português brasileiro
- Interface: Design clean e profissional
- Cores da marca: Bordô (#520B1B) e Bege (#C5A995)

## Atualizações Recentes

- **07/12/2024**: Limpeza do projeto - removidos arquivos Node.js desnecessários
- **07/12/2024**: Banco de dados PostgreSQL configurado via Replit
- **07/12/2024**: Upload de imagens para estampas (URL ou arquivo local) com limpeza automática de arquivos
- **07/12/2024**: Dashboard aprimorado com 10+ métricas e gráficos Chart.js (receita, pedidos por mês/status, cotações, etc.)
- **07/12/2024**: Script SQL completo em database/create_tables.sql para todas as tabelas
- **07/12/2024**: Configuração Railway otimizada (railway.json, Procfile, nixpacks.toml)
- **03/12/2024**: Upload de imagens de referência para cotações (além de URLs)
- **03/12/2024**: QR Code PIX integrado ao PDF de orçamento
- **03/12/2024**: Sistema profissional de orçamentos em PDF com logo Emunah e mensagem bíblica
- **03/12/2024**: Compartilhamento de orçamentos via WhatsApp com mensagem formatada
- **03/12/2024**: Envio de orçamento por email com PDF anexo
- **03/12/2024**: Refatoração do modelo Quote para suportar leads sem cadastro
- **03/12/2024**: Fluxo de aprovação de cotação com criação automática de pedido
- **03/12/2024**: Melhorias nas templates de cotações e pedidos
- **03/12/2024**: Configuração de credenciais via variáveis de ambiente
- **03/12/2024**: Logos EMUNAH copiados para static/images/

## Funcionalidades de PDF e Compartilhamento

O sistema agora permite:
1. **Baixar PDF profissional** do orçamento com:
   - Logo Emunah no cabeçalho
   - Dados completos do cliente e produtos
   - Informações de pagamento e PIX
   - Mensagem bíblica no rodapé ("Tudo posso naquele que me fortalece" - Filipenses 4:13)

2. **Enviar via WhatsApp** - Abre o WhatsApp com mensagem formatada contendo todos os detalhes do orçamento

3. **Enviar por Email** - Envia email com o PDF anexado (requer configuração SMTP)
