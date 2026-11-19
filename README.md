# sprint_11 — API-тесты сервиса «Доска»

Итоговый проект: независимые API-автотесты для https://qa-desk.education-services.ru/.
Запросы и ответы исследованы через фронтенд в Google Chrome DevTools → Network.
Для отправки API-запросов используется `requests`, для запуска тестов — `pytest`.

## Запуск

Нужен Python 3.10 или новее. Проект проверен на Python 3.12.4.

Из каталога `sprint_11`:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
```

Если окружение уже подготовлено:

```bash
.venv/bin/python -m pytest -v
```

Отдельная функциональность:

```bash
python -m pytest test/test_registration.py -v
python -m pytest test/test_edit_listing.py -v
```

Сохранение отчёта JUnit:

```bash
python -m pytest -v --junitxml=reports/pytest-results.xml
```

При необходимости адрес API переопределяется переменной `DESK_BASE_URL`:

```bash
DESK_BASE_URL=https://qa-desk.education-services.ru/api python -m pytest -v
```

Тестам нужен доступ к учебному сервису по HTTPS. Браузер нужен для исследования
трафика; при запуске готовых API-тестов браузер и Postman не требуются.

## Покрытие

- `test/test_registration.py`, `TestRegistration`: регистрация с новым email и
  отказ при регистрации уже занятого email.
- `test/test_login.py`, `TestLogin`: вход ранее зарегистрированного пользователя,
  проверка его идентификатора, email и типа полученного токена.
- `test/test_create_listing.py`, `TestCreateListing`: создание объявления в
  категории «Авто», проверка статуса и данных ответа.
- `test/test_edit_listing.py`, `TestEditListing`: изменение названия, описания и
  цены в трёх независимых параметризованных случаях; отказ в изменении чужого
  объявления с проверкой статуса и тела ошибки.
- `test/test_delete_listing.py`, `TestDeleteListing`: удаление собственного
  объявления с проверкой статуса и сообщения об успешном удалении.

Всего семь сценариев задания, девять тестовых случаев.

## Структура

```text
sprint_11/
├── api/
│   ├── base_api.py
│   ├── listing_api.py
│   └── user_api.py
├── helpers/
│   ├── assertions.py
│   ├── email_generator.py
│   └── user_helpers.py
├── test/
│   ├── test_registration.py
│   ├── test_login.py
│   ├── test_create_listing.py
│   ├── test_edit_listing.py
│   └── test_delete_listing.py
├── docs/
│   ├── API_RESEARCH.md
│   └── frontend-traffic.redacted.har
├── reports/
│   └── pytest-results.xml
├── conftest.py
├── config.py
├── data.py
├── models.py
├── pytest.ini
├── requirements.txt
└── urls.py
```

## Независимость и очистка

Все фикстуры имеют область действия одного теста. Для каждого нового пользователя
генерируется отдельный email с UUID4. Повторная регистрация использует email
пользователя, созданного фикстурой непосредственно для этого теста.

У каждого теста собственный пользователь и не более одного объявления.
Для отрицательного сценария фикстура `foreign_listing` создаёт второго
отдельного пользователя и принадлежащее ему объявление.
Чужие существующие объявления сервиса не изменяются.

Фикстура `listing_cleanup` удаляет созданные объявления и при падении проверки.
В тесте удаления успешно удалённое объявление снимается с очистки, чтобы не
отправлять повторный DELETE. Ошибки очистки отражаются в результате pytest.
Тестовые аккаунты остаются в учебной БД: удаление пользователей через
административные методы и общий сброс сервиса не используются.

Тестовые данные находятся в `data.py`, эндпоинты — в `urls.py`, модель
пользователя — в `models.py`, генератор email — в `helpers/email_generator.py`,
генератор регистрационных данных — в `helpers/user_helpers.py`, HTTP-методы —
в `api/`. В `conftest.py` находятся только фикстуры: HTTP-сессия, регистрация
пользователя, создание своих и чужих объявлений, очистка. Ошибки HTTP-запросов
предусловий и очистки обрабатываются через `raise_for_status()`, без `assert`.

Каждый тест выполняет один запрос к проверяемому API-методу и проверяет только
его ответ. Другие HTTP-запросы выполняются только в предусловиях и очистке.
В тестах нет условных ветвлений, `print` и закомментированного кода.

## Проверенный результат

19 ноября 2026 года полный запуск против учебного API завершился успешно:
**9 passed**. Машиночитаемый отчёт находится в `reports/pytest-results.xml`.
