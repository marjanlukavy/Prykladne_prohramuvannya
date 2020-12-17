# laba4
КАЧАЄМО ЧЕРЕЗ КЛОН або напряму цілим файлом(скачуємо .zip) git clone https://github.com/marjanlukavy/cs-oop/tree/main

СТВОРЮЄМО ВІРТУАЛЬНЕ СЕРЕДОВИЩЕ

pip install pipenv - якщо ще у вас немає virtualenv venv - (venv) назва нашого віртуального середовища

pipenv shell - щоб активувати наше середовище

pip install -r requirements.txt - управління пакетами Python

Збереження залежностей pip freeze > requirements.txt команду

Для запуску сервера ми напишемо gunicorn --reload "app:create_app()" (--reload перезапускає сервер автоматично), ("app:create_app()" (main) - наш файл),( (create_app()) - функція яку ми викликаємо)

для того щоб вийти з venv потрібно прописавти - deactivate
