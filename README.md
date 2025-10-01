# Project: Time Tracer

Есть две сущности: проект и запись.
Реализованы CRUD операции над этими сущностями.

**Сценарий использования:** пользователь создаёт проекты, а уже к ним привязывает записи о времени начала и длительности какого-то действия.

На данный момент не реализованы пользователи, но они будут добавлены в будущем вместе с авторизацией. Статистика, экспорт в CSV и тесты также будет добавлен позднее.

Репозиторий защищён от push'ей в main ветку с помощью pre-commit.

## Быстрый старт
```bash
docker-compose up --build
```

## Ритуал перед PR
```bash
ruff --fix .
black .
isort .
pytest -q
pre-commit run --all-files
```

## Тесты
```bash
pytest -q
```

## CI
В репозитории настроен workflow **CI** (GitHub Actions) — required check для `main`.
Badge добавится автоматически после загрузки шаблона в GitHub.

## Контейнеры
```bash
docker build -t secdev-app .
docker run --rm -p 8000:8000 secdev-app
# или
docker compose up --build
```

## Эндпойнты
- `GET /health` → `{"status": "ok"}`
- `POST /items?name=...` — демо-сущность
- `GET /items/{id}`

## Формат ошибок
Все ошибки — JSON-обёртка:
```json
{
  "error": {"code": "not_found", "message": "item not found"}
}
```

См. также: `SECURITY.md`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml`.
