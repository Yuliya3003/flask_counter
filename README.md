# Запуск проекта
### Сборка:
```bash
docker-compose up --build
```
### Работа
Приложение будет доступно по адресу http://localhost:5000.

Каждое обращение к / добавит запись в таблицу table_counter.

Посмотреть записи в таблице можно по адресу http://localhost:5000/view

### Для остановки работы приложения
```bash
docker-compose down --volumes
```