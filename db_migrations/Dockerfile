FROM postgres:14

COPY . /migrations

CMD ["bash", "-c", \
     "for f in $(ls /migrations/V*.sql | sort); do \
        echo \"Applying $f\"; \
        psql -U $POSTGRES_USER -d $POSTGRES_DB -f $f; \
      done"]