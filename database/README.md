# EMUNAH - Scripts de Banco de Dados

Este diretório contém os scripts para configuração e inicialização do banco de dados PostgreSQL.

## Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `init_db.sql` | Script SQL para criar todas as tabelas do banco de dados |
| `seed_data.sql` | Script SQL com dados de exemplo (fornecedores, estampas, produtos, clientes) |
| `init_railway.py` | Script Python para inicialização automática no Railway |

## Uso no Railway

### Opção 1: Inicialização Automática (Recomendado)

O Railway executa automaticamente a inicialização do banco através do `nixpacks.toml`:

```toml
[start]
cmd = "python database/init_railway.py && gunicorn app:app --bind 0.0.0.0:$PORT"
```

### Opção 2: Inicialização Manual via SQL

1. Acesse o console do PostgreSQL no Railway
2. Execute o script `init_db.sql` para criar as tabelas
3. Execute o script `seed_data.sql` para inserir dados de exemplo

```bash
psql $DATABASE_URL -f database/init_db.sql
psql $DATABASE_URL -f database/seed_data.sql
```

## Variáveis de Ambiente Necessárias

Configure estas variáveis no Railway:

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `DATABASE_URL` | Sim | URL de conexão PostgreSQL (gerada automaticamente pelo Railway) |
| `SECRET_KEY` ou `SESSION_SECRET` | Sim | Chave secreta para sessões Flask |
| `ADMIN_EMAIL` | Sim | Email do administrador |
| `ADMIN_PASSWORD` | Sim | Senha do administrador |
| `ADMIN_NAME` | Não | Nome do administrador (padrão: "Administrador") |
| `ADMIN_PHONE` | Não | Telefone do administrador |

## Estrutura das Tabelas

```
users           - Usuários do sistema (admin, vendedores)
clients         - Clientes cadastrados
suppliers       - Fornecedores de camisetas
products        - Produtos disponíveis
prints          - Estampas disponíveis
quotes          - Cotações/Orçamentos
orders          - Pedidos confirmados
order_items     - Itens dos pedidos
transactions    - Transações financeiras
email_logs      - Log de emails enviados
```

## Backup e Restore

### Criar Backup
```bash
pg_dump $DATABASE_URL > backup_emunah_$(date +%Y%m%d).sql
```

### Restaurar Backup
```bash
psql $DATABASE_URL < backup_emunah_YYYYMMDD.sql
```
