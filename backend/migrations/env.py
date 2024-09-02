from flask import current_app
from alembic import context
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('alembic.env')

# Alembic Config object
config = context.config

def get_engine_url():
    """Fetch the database URL from Flask's config."""
    try:
        url = current_app.extensions['migrate'].db.engine.url.render_as_string(hide_password=False).replace('%', '%%')
        logger.debug(f"Database URL: {url}")
        return url
    except AttributeError as e:
        logger.error(f"Error fetching engine URL: {e}")
        return str(current_app.extensions['migrate'].db.engine.url).replace('%', '%%')

# Set the SQLAlchemy URL option dynamically
config.set_main_option('sqlalchemy.url', get_engine_url())

# Add your model's MetaData object here
from app import db
from app.models import User, Project

target_metadata = db.metadata
print(target_metadata)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    logger.debug(f"Running migrations offline with URL: {url}")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = db.engine
    logger.debug("Connecting to the database for online migrations.")
    
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
