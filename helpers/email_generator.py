from uuid import uuid4


def generate_email():
    """Возвращает новый email для каждого вызова, включая параллельные запуски."""
    return f"sprint11.{uuid4().hex}@example.com"
