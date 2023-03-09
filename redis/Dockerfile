ARG REDIS

FROM redis/redis-stack:${REDIS}

HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 \
    CMD redis-cli ping | grep PONG
