FROM postgres:14

COPY . /migrations

CMD ["bash", "-c", "\
  export PGHOST=$DB_HOST PGPORT=$DB_PORT \
    PGUSER=$DB_USER PGPASSWORD=$DB_PASSWORD PGDATABASE=$DB_NAME; \
  echo 'Waiting for PostgreSQL...'; \
  until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do sleep 2; done; \
  echo 'Applying migrations...'; \
  for f in $(ls /migrations/V*.sql | sort); do \
    echo \"Applying $f\"; \
    psql -f $f || echo \"Migration $f failed, continuing...\"; \
  done; \
  echo 'Migrations completed'"]