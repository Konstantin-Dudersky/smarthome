ARG POSTGRE_VER
ARG TIMESCALEDB_VER
FROM timescale/timescaledb:${TIMESCALEDB_VER}-pg${POSTGRE_VER}
COPY db/init.sql /docker-entrypoint-initdb.d/
