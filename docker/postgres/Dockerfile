FROM postgres:14

# Install pg_cron extension
RUN apt-get update && apt-get install -y postgresql-14-cron

# Copy initialization SQL script
COPY init.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432