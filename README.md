# Datawiz_demo

Приложение развернуто на Heroku: https://dw-demo.herokuapp.com

Зайти можно под тестовым пользователем: логин test1@mail.com, пароль qwerty

Карта сайта:
- [вход для зарегистрированного пользователя] (http://dw-demo.herokuapp.com/login)
- [регистрация нового пользователя] (http://dw-demo.herokuapp.com/register)
- [общие сведенья пользователя] (http://dw-demo.herokuapp.com)
- [основные показатели] (http://dw-demo.herokuapp.com/general)
- [отчет по динамике изменения продаж] (http://dw-demo.herokuapp.com/difference)

<h3>Преимущества</h3>
- Для обновления данных на странице используется AJAX.

- Запросы к API кешируются с помощью Redis (5 минут результат запроса будет находится в кеше), по этому
повторная выборка по тому же интервалу дат будет происходить мгновенно.

- Для расчетов используется библиотека Pandas

- Переделана модель пользователя, которая теперь использует email вместо имени пользователя и хранит API key для 
доступа к Datawiz API.

<h3>Недостатки</h3>
- нету пагинации, по этому вывод больших таблиц делает страницу гигантской

- медленный ответ от Datawiz API и громоздкие операции над большим масивом данных заставляет очень долго ожидать результат.

- бесплатный тарифный план Heroku не предполагает нахождения приложения постоянно в активном состоянии, по этому, после 
некоторого промежутка времени, приложение отправляется в сон и требуется время на его повторную активацию.


<h3>Замечания</h3>

* Библиотека python-dwapi содержат ошибки (по большей части похоже на хвосты после портирования с Python 2), 
по этому запуск приложения на Heroku "из коробки" не возможен. Решил проблему форком библиотеки ([ссылка на форк] (github.com/Charnelx/pythonAPI)), исправлением ошибок
и установкой её на Heroku из моего репозитария. Такой метод плох из-за сложности обновлений. Для обновления библиотеки
неоходимо сначала заставить Heroku перестроить окружение, удалить библиотеку вручную и затем перестроить окружение снова.
Просто удалить библиотеку не получится - Heroku мгновенно восстанавливает компоненты, соответственно и библиотека после удаления
опять будет на своем месте.

* В задаче к основным показателям требовалось добавить средний чек. Если верить интернетам, то средний чек вычисляется по формуле:

 > Средний чек = выручка / количество чеков

  Показателя выручки в возвращаемых dwapi данных нету, но есть показатель "средняя цена за единицу товара (price)" - в некотором приближении можно утверждать, что:
  
  > Выручка = количество проданных товаров * цена товара
  
  Проблема в том, что включая в запрос к dwapi колонку price, в ответ сервер возвращает 500-й код ошибки. То-же самое возвращается например при попытке получить колонку "self_price_per_product". 
  
  Как результат, вместо среднего чека я произвел расчет средней прибыли на чек:
  
  > прибыль / количество чеков
  
  Это конечно ~~совсем не то~~ не совсем то, что хотелось получить, но надеюсь моих объяснений достаточно для понимания проблемы.
