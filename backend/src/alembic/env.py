from logging.config import fileConfig
import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = str(Path(__file__).parent.parent.absolute())
sys.path.append(src_path)

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 모델 import
from domain.entities.user import User, BusinessProfile
from domain.entities.user_type import UserType
from config.database import Base
from config.settings import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# DB URL 설정 덮어쓰기
config.set_main_option("sqlalchemy.url", settings.sync_database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


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
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
