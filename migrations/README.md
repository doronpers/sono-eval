# Database Migrations

This directory contains database migrations managed by Alembic.

## Setup

Alembic is already configured. The database URL is automatically loaded from
your `.env` configuration.

## Common Commands

### Create a new migration

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Create empty migration template
alembic revision -m "Description of changes"
```

### Apply migrations

```bash
# Upgrade to latest version
alembic upgrade head

# Upgrade by one version
alembic upgrade +1

# Downgrade by one version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade <revision>
```

### Check migration status

```bash
# Show current revision
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic history --verbose
```

## Migration Best Practices

1. **Always review auto-generated migrations** before applying them
2. **Test migrations on a copy of production data** before deploying
3. **Write reversible migrations** (both upgrade and downgrade)
4. **Keep migrations small and focused** on one change
5. **Add descriptive commit messages** explaining the change

## Example Migration

```python
"""add user authentication table

Revision ID: 001
Revises:
Create Date: 2026-01-11
"""
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )

def downgrade() -> None:
    op.drop_table('users')
```

## Troubleshooting

### "Can't locate revision identified by 'xxxx'"

- Check that all migration files are present in `migrations/versions/`
- Ensure the database `alembic_version` table is correct

### "Target database is not up to date"

- Run `alembic upgrade head` to apply pending migrations

### "Multiple heads detected"

- Merge branches with `alembic merge heads -m "merge branches"`

## Documentation

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
