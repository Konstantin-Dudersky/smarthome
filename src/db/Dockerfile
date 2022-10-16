ARG POSTGRE_VER=14.5
ARG TIMESCALEDB_VER=2.8.1
FROM timescale/timescaledb-ha:pg${POSTGRE_VER}-ts${TIMESCALEDB_VER}-latest \
    AS sh_db
COPY db/init.sql /docker-entrypoint-initdb.d/
