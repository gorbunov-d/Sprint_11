USER_PASSWORD = "DeskSprint123!"

LISTING_DATA = {
    "name": "Тестовое объявление sprint_11",
    "category": "Авто",
    "condition": "Новый",
    "city": "Москва",
    "description": "Временное объявление для API-автотестов sprint_11",
    "price": 1000,
}

LISTING_CHANGES = [
    ("name", "Изменённое название sprint_11"),
    ("description", "Изменённое описание sprint_11"),
    ("price", 2500),
]

DUPLICATE_EMAIL_ERROR = {
    "statusCode": 400,
    "message": "Почта уже используется",
}

FOREIGN_LISTING_ERROR = {
    "message": "Оффер не найден или у вас нет прав на его редактирование",
    "error": "Unauthorized",
    "statusCode": 401,
}

DELETE_SUCCESS = {"message": "Объявление удалено успешно"}
