import json
import logging
import logging.config
from typing import Any, Dict, List

# Поля, которые нужно маскировать в логах
SENSITIVE_FIELDS = {"password", "token", "access_token", "authorization"}


class SensitiveDataFilter(logging.Filter):
    """
    Фильтр для маскирования чувствительных данных в записях лога
    """

    def filter(self, record: logging.LogRecord) -> bool:
        # Статический анализатор, ты доволен?? Так красиво и читаемо??
        data_to_process = record.__dict__.get("data")

        if isinstance(data_to_process, dict):
            # Создаем копию, чтобы не изменять оригинальные данные в коде
            record.data = self._mask_sensitive_data(data_to_process.copy())

        return True

    def _mask_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        for key, value in data.items():
            if key.lower() in SENSITIVE_FIELDS and isinstance(value, str):
                data[key] = "[SENSITIVE]"
            elif isinstance(value, dict):
                data[key] = self._mask_sensitive_data(value)
            elif isinstance(value, list):
                data[key] = self._mask_list(value)
        return data

    def _mask_list(self, data: List[Any]) -> List[Any]:
        return [
            self._mask_sensitive_data(item) if isinstance(item, dict) else item for item in data
        ]


class JsonFormatter(logging.Formatter):
    """
    Форматер для вывода логов в формате JSON
    """

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }

        # Добавляем кастомные данные из extra, если они есть
        if data := record.__dict__.get("data"):
            log_record.update(data)

        # Добавляем информацию об исключении, если она есть
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(log_record, ensure_ascii=False)


def get_logging_config() -> dict:
    """Возвращает словарь конфигурации логирования"""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "sensitive_data_filter": {
                # Указываем путь к нашему классу
                "()": "app.core.logging_config.SensitiveDataFilter",
            },
        },
        "formatters": {
            "json": {
                # Указываем путь к нашему классу
                "()": "app.core.logging_config.JsonFormatter",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
                "filters": ["sensitive_data_filter"],
                "stream": "ext://sys.stderr",  # Явно указываем поток вывода
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
    }


def setup_logging():
    logging.config.dictConfig(get_logging_config())
