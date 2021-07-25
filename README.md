# Тестовое задание DomClick

## Демо

### CRM для регистрации и обработки входящих заявок от пользователей

- [GraphQL API](https://domclick.srezanova.me/graphql/)
- [Задеплоенное приложение](https://domclick.srezanova.me/)

**Работа сайта (частичный функционал для отображения возможностей сервиса):**

На [домашней странице](https://domclick.srezanova.me/) отображены все заявки с фильтрами.

![home](img/home.png)

Можем создать заявку:

<img src="img/new-task.png" alt="new-task" width="350"/>

Отредактировать и удалить ее:

![edit](img/edit.png)

## GraphQL API

Реализован с помощью Django и библиотеки [graphene-django](https://docs.graphene-python.org/projects/django/en/latest/).

### Аутентификация

Аутентификация реализована с помощью JWT токена и библиотеки [django-graphql-jwt](https://github.com/flavors/django-graphql-jwt).

Мутация `register` используется для регистрации сотрудников, почта и пароль – обязательные поля:

![register](img/register.png)

Мутация `login` аутентифицирует сотрудника:

![login](img/login.png)

Мутация `updateUser` используется для смены почты сотрудника:

![updateUser](img/updateUser.png)

Кверя `me` возвращает данные текущего сотрудника:

![me](img/me.png)

### Модель клиента

Поля:

1. ID
2. Телеграм ID
3. Номер телефона
4. Имя

Кверя `allCustomers` возвращает всех клиентов:

![allCustomers](img/allCustomers.png)

Кверя `customerById` возращает клиента по ID.

![customerById](img/customerById.png)

Мутация `createCustomer` создает запись клиента. Поле номер телефона уникальное.

![createCustomer](img/createCustomer.png)

Мутация `updateCustomer` меняет запись клиента. Для изменения данных необходимо ввести номер телефона клиента. Если у клиента поменялся номер телефона - создать новую карточку.

![updateCustomer](img/updateCustomer.png)

Мутация `deleteCustomer` удаляет запись клиента.

![deleteCustomer](img/deleteCustomer.png)

### Модель заявки

1. ID
2. Дата создания
3. Клиент
4. Ответственный сотрудник по заявке
5. Тип заявки:
   - Консультация
   - Диагностика
   - Ремонт
   - Прочее
6. Статус заявки:
   - Принято
   - В работе
   - Готово
   - Закрыто
7. Дополнительная информация (описание неисправности, результат консультации и т.д.)

Кверя `allTasks` возвращает все заявки.

**Фильтры**

- по клиентам(по номеру телефона)
- по статусам (одному или нескольким)
- по категориям
- по дате создания заявки
- по интервалу дат

![allTasksNoFilters](img/allTasksNoFilters.png)

![allTasksFiltersDate](img/allTasksFiltersDate.png)

Кверя `taskById` возвращает заявку по ID.

![taskById](img/taskById.png)

Мутация `createTask` создает заявки. Клиент заполняется по полю номер телефона. Если такого клиента не существует в базе - создается новая карточка. Данные пользователя как ответственного сотрудника по заявке автоматически заполняются по данным входа.

![createTask](img/createTask.png)

Мутация `updateTask` изменяет заявку по ее ID. Доступные поля для изменения: статус, тип заявки, описание.

![updateTask](img/updateTask.png)

Мутация `deleteTask` удаляет заявку по ID.

![deleteTask](img/deleteTask.png)

### Telegram bot

Функционал телеграм-бота:
При старте бот предлагает ввести телефон, в БД делается запись по клиенту с данными: telegram_id, номер телефона, имя из телеграмма.

![bot_start](img/bot_start.png)

При любом вводе данных бот отправляет список всех заявок.

![deleteTask](img/deleteTask.png)

При изменении статуса заявки бот отправляет уведомление.

![bot_update](img/bot_update.png)
