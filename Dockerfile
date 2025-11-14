# Установка зависимостей и сборка
FROM python:3.11-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Копируем только файлы с зависимостями, чтобы кешировать этот слой
COPY ./requirements.txt .

# Создаем wheels для всех зависимостей
RUN pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt


# Runtime образ
FROM python:3.11-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Создаем непривилегированного пользователя и группу для запуска приложения
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y curl --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

COPY ./app ./app
COPY ./alembic.ini .
COPY ./migrations ./migrations
COPY ./docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

# Даем права на выполнение скрипту
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Меняем владельца всех файлов на нашего непривилегированного пользователя
RUN chown -R appuser:appgroup /app

# Переключаемся на непривилегированного пользователя
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
