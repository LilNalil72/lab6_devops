FROM postgres:14

COPY . /migrations

CMD ["bash", "-c", "\
  export PGHOST=$DB_HOST PGPORT=$DB_PORT \
    PGUSER=$DB_USER PGPASSWORD=$DB_PASSWORD PGDATABASE=$DB_NAME; \
  for f in $(ls /migrations/V*.sql | sort); do \
    echo \"Applying $f\"; \
    psql -f $f; \
  done"]