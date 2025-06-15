FROM postgres:14

# Установка дополнительных утилит для отладки
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY . /migrations

# Создаем скрипт для выполнения миграций
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "Waiting for PostgreSQL to be ready..."\n\
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do\n\
  echo "PostgreSQL is unavailable - sleeping"\n\
  sleep 2\n\
done\n\
\n\
echo "PostgreSQL is up - executing migrations"\n\
\n\
export PGHOST=$DB_HOST PGPORT=$DB_PORT PGUSER=$DB_USER PGPASSWORD=$DB_PASSWORD PGDATABASE=$DB_NAME\n\
\n\
# Создаем таблицу версий если не существует\n\
psql -c "CREATE TABLE IF NOT EXISTS schema_version (version INT PRIMARY KEY, applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"\n\
\n\
for f in $(ls /migrations/V*.sql | sort -V); do\n\
  VERSION=$(basename $f | sed "s/V\\([0-9]*\\)__.*/\\1/")\n\
  echo "Checking migration version $VERSION"\n\
  \n\
  # Проверяем, была ли уже применена эта миграция\n\
  EXISTS=$(psql -t -c "SELECT COUNT(*) FROM schema_version WHERE version = $VERSION;" | xargs)\n\
  \n\
  if [ "$EXISTS" = "0" ]; then\n\
    echo "Applying migration: $f"\n\
    psql -f $f\n\
    \n\
    # Записываем версию в таблицу, если её там нет\n\
    if ! grep -q "INSERT INTO schema_version" $f; then\n\
      psql -c "INSERT INTO schema_version (version) VALUES ($VERSION) ON CONFLICT (version) DO NOTHING;"\n\
    fi\n\
    \n\
    echo "Migration $f applied successfully"\n\
  else\n\
    echo "Migration $f already applied, skipping"\n\
  fi\n\
done\n\
\n\
echo "All migrations completed successfully"' > /run_migrations.sh

RUN chmod +x /run_migrations.sh

CMD ["/run_migrations.sh"]