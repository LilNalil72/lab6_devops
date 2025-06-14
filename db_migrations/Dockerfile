FROM postgres:14

COPY . /migrations

CMD ["bash", "-c", "\
  for f in $(ls /migrations/V*.sql | sort); do \
    echo \"Applying $f\"; \
    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f $f; \
  done"]
