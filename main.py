"""
Main entry point for Gunicorn.
Initializes the database and exposes the Flask app.
"""
import logging

logging.basicConfig(level=logging.INFO)

from app import app, init_db

# Initialize database when loaded by gunicorn
try:
    init_db()
except Exception as e:
    logging.error(f"Database initialization error (non-fatal): {e}")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
