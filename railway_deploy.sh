#!/bin/bash
# EMUNAH - Railway Deployment Script

echo "================================================"
echo "EMUNAH - Sistema de Vendas e Orçamentos"
echo "Railway Deployment Script"
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    exit 1
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
python3 -c "
from app import app, db, init_db
with app.app_context():
    db.create_all()
    print('Database tables created successfully!')
"

# Initialize database with sample data if needed
echo "Initializing database..."
python3 -c "
from app import init_db
init_db()
"

echo ""
echo "================================================"
echo "Deployment preparation complete!"
echo ""
echo "Make sure you have set the following environment variables in Railway:"
echo "  - DATABASE_URL (PostgreSQL connection string)"
echo "  - SECRET_KEY or SESSION_SECRET (for session security)"
echo "  - ADMIN_EMAIL (admin user email)"
echo "  - ADMIN_PASSWORD (admin user password)"
echo ""
echo "Optional email configuration:"
echo "  - MAIL_SERVER (SMTP server, default: smtp.gmail.com)"
echo "  - MAIL_PORT (SMTP port, default: 587)"
echo "  - MAIL_USERNAME (SMTP username)"
echo "  - MAIL_PASSWORD (SMTP password or app password)"
echo "  - MAIL_DEFAULT_SENDER (sender email address)"
echo "================================================"
