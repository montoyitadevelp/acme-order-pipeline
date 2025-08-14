import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import async_engine_from_config

from sqlalchemy import pool

from alembic import context
from src.config.database import DATABASE_URL, Base
# Import models to ensure they are registered with SQLAlchemy
from src.product.models import Product
from src.inventory.models import Inventory

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
section = config.config_ini_section
config.set_section_option(section, "DB_URL", DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """
    The function `do_run_migrations` configures a database connection and runs migrations using the
    provided context.

    :param connection: The `connection` parameter typically refers to the database connection that will
    be used to run the migrations. This connection allows the migration scripts to interact with the
    database to make necessary changes to its schema
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """
    The function `run_async_migrations` connects to a database asynchronously, runs migrations
    synchronously, and disposes of the connection.
    """
    section_config = config.get_section(config.config_ini_section) or {}
    connectable = async_engine_from_config(
        section_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online():
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
