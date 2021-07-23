# CRM для регистрации и обработки входящих заявок от клиентов

## Пользователи

Пользователями сервиса являются сотрудники компании.

### Регистрация и аутентификация

Чтобы зарегистрировать пользователя необходимо воспользоваться **register Mutation**.

Необходимые поля для регистрации: почта и пароль.

![Register](img/register.png)

Для входа на сервис используется JWT Token. Получаем его через **login Mutation**.

![Login](img/login.png)

Пользователь может поменять свою почту с помощью **updateUser Mutation**

![updateUser](img/updateUser.png)

### Получение данных о пользователях

Пользователь может получить свои данные с помощью **me Query**.

![me](img/me.png)

## Заявки

### Структура заявки

1. Клиент

2. Ответственный сотрудник по заявке

3. Техника покупателя

4. Тип заявки:

   - Консультация
   - Диагностика
   - Ремонт
   - Возврат
   - Жалоба
   - Прочее

5. Статус заявки:

   - Открыта
   - Запланирована
   - Отменена
   - Закрыта

6. Описание проблемы от клиента

7. Текущее/окончательное решение проблемы

8. Контактные данные пользователя, если он не зарегистрирован

9. Сообщение для клиента, которое используется в системе оповещений.

### Получение данных о заявках

Пользователь / сотрудник может получить информацию по всем своим заявкам с помощью **myRequests Query**.

![myRequests](img/myRequests.png)

Пользователь / сотрудник может получить данные заявки по ее ID с помощью **request Query**.

![request](img/request.png)

Сотрудники могут получить доступ ко всем заявкам компании с помощью **allRequests Query**.

### Фильтрация заявок

Сотрудники могут фильтровать заявки:

- по статусам и категориям с помощью **allRequestsFilterStatusAndCategory Query** или **myRequestsFilterStatusAndCategory Query**.

![allRequestsFilterStatusAndCategory](img/allRequestsFilterStatusAndCategory.png)

![myRequestsFilterStatusAndCategory](img/myRequestsFilterStatusAndCategory.png)

- по статусам или категориям с помощью **allRequestsFilterStatusOrCategory Query** или **myRequestsFilterStatusOrCategory Query**.

![allRequestsFilterStatusOrCategory_category](img/allRequestsFilterStatusOrCategory_category.png)

![allRequestsFilterStatusOrCategory_status](img/allRequestsFilterStatusOrCategory_status.png)

![myRequestsFilterStatusOrCategory](img/myRequestsFilterStatusOrCategory.png)

- по дате или интервалу дат с помощью **allRequestsFilterDate Query** или **myRequestsFilterDate Query**.

![allRequestsFilterDate](img/allRequestsFilterDate.png)

![allRequestsFilterDate_range](img/allRequestsFilterDate_range.png)

![myRequestsFilterDate](img/myRequestsFilterDate.png)

![myRequestsFilterDate_range](img/myRequestsFilterDate_range.png)

### Создание заявок

Пользователь / сотрудник могут создать заявки с помощью **createRequestClient Mutation** и **createRequestClient Mutation**.

У клиента есть доступ к полям: техника, проблема. Данные клиента автоматически заполняются по данным входа.

![createRequestClient](img/createRequestClient.png)

У сотрудников есть доступ ко всем полям. Данные сотрудника автоматически заполняются по данным входа.

![createRequestEmployee](img/createRequestEmployee.png)

### Изменение заявок

Изменить заявку может только сотрудник ответственный за данную заявку с помощью **updateRequest Mutation**.

У администратора есть доступ ко всем заявкам.

![updateRequest](img/updateRequest.png)

### Удаление заявок

Удалить заявку может только администратор с помощью **deleteRequest Mutation**.

![deleteRequest](img/deleteRequest.png)
