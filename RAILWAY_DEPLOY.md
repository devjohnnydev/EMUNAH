# Deploy no Railway - Emunah Sistema

## Configuração do Railway

### 1. Criar Novo Projeto no Railway
1. Acesse [railway.app](https://railway.app)
2. Faça login com sua conta GitHub
3. Clique em "New Project" > "Deploy from GitHub repo"
4. Selecione este repositório

### 2. Adicionar Banco de Dados PostgreSQL
1. No projeto Railway, clique em "New"
2. Selecione "Database" > "Add PostgreSQL"
3. O Railway vai configurar automaticamente a variável `DATABASE_URL`

### 3. Configurar Variáveis de Ambiente
No painel do Railway, vá em "Variables" e adicione:

**Obrigatórias:**
```
SECRET_KEY=sua-chave-secreta-aqui-gere-uma-segura
SESSION_SECRET=outra-chave-secreta-para-sessao
```

**Admin (recomendadas):**
```
ADMIN_EMAIL=seu-email@empresa.com
ADMIN_PASSWORD=sua-senha-segura
ADMIN_NAME=Seu Nome
ADMIN_PHONE=11999999999
```

**Email (opcionais):**
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=sua-senha-de-app
MAIL_DEFAULT_SENDER=noreply@emunah.com
```

### 4. Deploy Automático
O Railway fará deploy automaticamente quando você der push para o repositório.

O script `database/init_railway.py` será executado automaticamente e irá:
- Criar todas as tabelas do banco de dados
- Criar o usuário administrador
- Popular 30 estampas evangélicas Emunah
- Adicionar fornecedores e clientes de exemplo

## Estrutura do Projeto

```
emunah/
├── app.py                    # Aplicação Flask principal
├── main.py                   # Ponto de entrada
├── templates/                # Templates Jinja2
├── static/                   # Arquivos estáticos (CSS, JS, imagens)
├── database/
│   ├── init_railway.py       # Script de inicialização Railway
│   ├── init_db.sql           # Schema SQL
│   └── seed_data.sql         # Dados iniciais
├── seed_prints.py            # Script para popular estampas
├── deploy_railway.py         # Script de deploy completo
├── railway_deploy.sh         # Script bash de deploy
├── Procfile                  # Configuração de processo
├── railway.json              # Configuração do Railway
├── runtime.txt               # Versão do Python
├── requirements.txt          # Dependências Python
└── pyproject.toml            # Configuração do projeto
```

## Scripts de Deploy

### Via Python (recomendado)
```bash
python deploy_railway.py
```

### Via Bash
```bash
chmod +x railway_deploy.sh
./railway_deploy.sh
```

### Popular apenas estampas
```bash
python seed_prints.py
```

## Comandos Úteis

### Executar localmente
```bash
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

ou

```bash
python app.py
```

### Acessar o sistema
- URL local: http://localhost:5000

## Primeiro Acesso (Produção)

O sistema cria automaticamente um usuário administrador inicial quando não há usuários no banco de dados.

**IMPORTANTE**: Configure as variáveis ADMIN_EMAIL e ADMIN_PASSWORD antes do primeiro deploy para definir suas credenciais personalizadas.

Se não configurar, será criado um admin temporário com credenciais aleatórias (verifique os logs do Railway).

## Funcionalidades

- Dashboard com métricas e gráficos
- Gestão de Fornecedores
- **30 Estampas Evangélicas Emunah** pré-cadastradas
- Cotações com fornecedores
- Orçamentos para clientes (com PIX QR Code)
- Pedidos e acompanhamento de produção
- Cadastro de Clientes
- Envio de emails (cotações e confirmações)
- Autenticação de usuários com níveis de acesso

## Paleta de Cores

A marca Emunah utiliza as seguintes cores:

| Cor | Código | Uso |
|-----|--------|-----|
| **Borgonha** | #520B1B | Primária - logo e destaques |
| **Areia** | #E5D2C4 | Secundária - fundos |
| **Creme Suave** | #C5A995 | Complementar - detalhes |

## Suporte

Para dúvidas sobre o sistema, entre em contato com o desenvolvedor.
