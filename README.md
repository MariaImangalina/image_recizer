# ImageResizer

Приложение для изменения размера изображений, написано на Python на основе фреймворка Django. Частично покрыто тестами.

## Включает в себя:

1) стартовую страницу со списком загруженных изображений

2) страницу загрузки с возможностью аплоада из файла или по URL

3) страницу изображения. Показывает изображение в оригинальном размере, после заполнении формы выводит страницу обновленного изображения заданного размера.

Изменить можно высоту, ширину или оба значения. В последнем случае, при нарушении пропорций расчет будет сделан на основе большей стороны



## Запуск

1) Создайте новое окружение: `python3 -m venv venv`

2) Активируйте его: `venv\Scripts\activate`

3) Cоздайте новую папку и клонируйте в нее репозиторий: `git clone https://github.com/MariaImangalina/image_recizer.git`

4) Установите зависимости: `pip install -r requirements.txt`

5) Запустите локальный сервер: `python manage.py runserver`
будет доступен здесь -  http://127.0.0.1:8000


6) Запуск тестов: `python manage.py test`
