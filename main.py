"""
Main entry point for Gunicorn.
Initializes the database and exposes the Flask app.
"""
import os
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from app import app, init_db

def initialize_with_retry(max_retries=5, delay=3):
    """Initialize database with retry logic for container startup."""
    for attempt in range(max_retries):
        try:
            logger.info(f"Database initialization attempt {attempt + 1}/{max_retries}")
            init_db()
            logger.info("Database initialized successfully!")
            return True
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.error("All initialization attempts failed. App will start without seed data.")
    return False

# Initialize database when loaded by gunicorn
# Use retry logic to handle database startup delays in containers
initialize_with_retry()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
