
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from config import DB_URL
# 1. Load the .env file from your backend directory


from database.db import Base
from database.models import UserData, UserAgentOutputs

config = context.config

# 2. Overwrite the ini-file URL with your DB_URL from .env
# This ensures Alembic uses the 'postgresql+psycopg2://' driver
postgres_url = DB_URL
if postgres_url:
    # Escape '%' by replacing it with '%%' for Alembic's config parser
    escaped_url = postgres_url.replace("%", "%%")
    config.set_main_option("sqlalchemy.url", escaped_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def include_object(object, name, type_, reflected, compare_to):
    """
    Control which objects Alembic should 'see' and 'manage'.
    """
    # List of tables managed by LangGraph that we want to protect
    langgraph_tables = [
        "checkpoints",
        "checkpoint_blobs",
        "checkpoint_migrations",
        "checkpoint_writes"
    ]

    if type_ == "table" and name in langgraph_tables:
        return False  # Do not include these in the migration generation

    return True

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
        include_object=include_object,  # Add this line
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
