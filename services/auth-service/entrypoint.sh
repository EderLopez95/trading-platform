#!/bin/sh

echo "Waiting for PostgreSQL..."

DB_HOST=$(echo $DATABASE_URL | sed -E 's|.*@([^:]+):.*|\1|')
DB_PORT=$(echo $DATABASE_URL | sed -E 's|.*:([0-9]+)/.*|\1|')

echo "DB_HOST=$DB_HOST"
echo "DB_PORT=$DB_PORT"

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "Running migrations..."

until alembic upgrade head; do
  echo "Migration failed, retrying in 2s..."
  sleep 2
done

echo "Starting auth service..."

python -m main
