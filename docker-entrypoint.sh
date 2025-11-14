#!/bin/sh

set -e

# миграции alembic
echo "Running database migrations..."
alembic upgrade head

# выполняем основную команду контейнера (CMD)
echo "Starting application..."
exec "$@"