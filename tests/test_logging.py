import logging
from fastapi.testclient import TestClient

def test_password_is_redacted_in_logs_on_failed_login(client: TestClient, caplog):
    """
    Проверяет, что пароль маскируется в логах при неудачной попытке входа
    """
    # Устанавливаем уровень логирования, который будем перехватывать
    with caplog.at_level(logging.WARNING):
        # Выполняем заведомо неудачный запрос на вход
        client.post(
            "/api/v1/auth/login",
            json={"username": "testuser", "password": "wrong_password"},
        )

    assert len(caplog.records) > 0, "No logs were captured"

    # Ищем нужную нам запись
    failed_login_record = None
    for record in caplog.records:
        if "Failed login attempt" in record.message:
            failed_login_record = record
            break
    
    assert failed_login_record is not None, "Failed login log record not found"
    
    # Проверяем уровень лога
    assert failed_login_record.levelname == "WARNING"
    
    # Проверяем, что секрет не попал в отформатированное сообщение
    assert "wrong_password" not in caplog.text
    
    # Проверяем данные, которые были обработаны фильтром
    log_data = failed_login_record.data
    assert isinstance(log_data, dict)
    assert log_data.get("password") == "[SENSITIVE]"
    assert log_data.get("username") == "testuser"
