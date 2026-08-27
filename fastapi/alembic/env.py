from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from app.core.config import settings
from app.vectorstore.database import Base
from app.vectorstore import models


# Alembic Config object
config = context.config


# Use database URL from application settings
config.set_main_option(
    "sqlalchemy.url",
    settings.database_url.replace("%", "%%"),
)


# Configure Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# SQLAlchemy metadata for autogenerate
target_metadata = Base.metadata


def include_object(object, name, type_, reflected, compare_to):
    """
    Tell Alembic which database objects should be included
    during autogeneration.

    The database already contains tables created by Django.
    Those tables are not part of our SQLAlchemy metadata, so
    Alembic must ignore them instead of trying to remove them.
    """

    if type_ == "table" and reflected:
        django_tables = {
            "auth_group",
            "auth_group_permissions",
            "auth_permission",
            "auth_user",
            "auth_user_groups",
            "auth_user_user_permissions",
            "django_admin_log",
            "django_content_type",
            "django_migrations",
            "django_session",
        }

        if name in django_tables:
            return False

    return True


def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in online mode.
    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()