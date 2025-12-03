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

```
SECRET_KEY=sua-chave-secreta-aqui-gere-uma-segura
FLASK_DEBUG=False
```

### 4. Deploy Automático
O Railway fará deploy automaticamente quando você der push para o repositório.

## Estrutura do Projeto

```
emunah/
├── app.py              # Aplicação Flask principal
├── templates/          # Templates Jinja2
├── static/             # Arquivos estáticos (CSS, JS, imagens)
├── Procfile            # Configuração de processo
├── railway.json        # Configuração do Railway
├── runtime.txt         # Versão do Python
└── pyproject.toml      # Dependências Python
```

## Comandos Úteis

### Executar localmente
```bash
python app.py
```

### Acessar o sistema
- URL local: http://localhost:5000

### Primeiro Acesso (Produção)
O sistema cria automaticamente um usuário administrador inicial quando não há usuários no banco de dados.
**IMPORTANTE**: Após o primeiro login, altere imediatamente a senha do administrador através da gestão de usuários.

Para configurar credenciais personalizadas, defina as variáveis de ambiente antes do primeiro deploy:
```
ADMIN_EMAIL=seu-email@empresa.com
ADMIN_PASSWORD=sua-senha-segura
```

## Funcionalidades

- Dashboard com métricas e gráficos
- Gestão de Fornecedores
- Cadastro de Estampas
- Cotações com fornecedores
- Orçamentos para clientes
- Pedidos e acompanhamento de produção
- Cadastro de Clientes
- Autenticação de usuários

## Suporte

Para dúvidas sobre o sistema, entre em contato com o desenvolvedor.
