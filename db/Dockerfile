ARG POSTGRE_VER
ARG TIMESCALEDB_VER
FROM timescale/timescaledb-ha:pg${POSTGRE_VER}-ts${TIMESCALEDB_VER}-latest \
    AS sh_db
COPY db/init.sql /docker-entrypoint-initdb.d/
