![Geekbrains](https://frontend-scripts.hb.bizmrg.com/unique-hf/svg/logo_gb_dark_mobile.svg)

## Дипломная работа - Веб-приложение "Менеджер паролей"

* Студенты:
    * [**Константин Пивнов**](https://gb.ru/users/ccf373b9-ace0-4a52-a857-5226eb7672cc)
    * [**Елизавета Кузьмина**](https://gb.ru/users/c1e605db-903b-4578-9426-ed6717dd0331)

---

### Инструкция по использованию:

* Клонировать репозиторий на локальный компьютер:

      git clone https://github.com/vaproloff/pysSwordManager.git

* Перейти в директорию репозитория, создать и активировать виртуальное окружение:

      cd pysSwordManager

      python -m venv venv     # Windows
      python3 -m venv venv    # MacOS/Linux

      venv\Scripts\activate       # Windows
      source venv/bin/activate    # MacOS/Linux

* Установить все зависимости:

      pip install -r requirements.txt

* Сгенерировать симметричный ключ шифрования для хранения паролей в консоли Python:

      python     # Windows
      python3    # MacOS/Linux

      from cryptography.fernet import Fernet
      Fernet.generate_key()

      exit()

* Добавить файл `pysSword/.env` c информацией:

      CRYPTO_KEY='ваш_ключ_шифрования_паролей'
      EMAIL_HOST='адрес_сервера_исходящей_почты'
      EMAIL_PORT=порт_сервера_исходящей_почты
      EMAIL_HOST_USER='имя_пользователя_сервера_исходящей_почты'
      EMAIL_HOST_PASSWORD='пароль_сервера_исходящей_почты'

* Применить миграции к базе данных:

      cd pysSword
      python manage.py migrate     # Windows
      python3 manage.py migrate    # MacOS/Linux

* При необходимости использования админ-панели выполнить команду и следовать инструкциям по созданию суперпользователя:

      python manage.py createsuperuser     # Windows
      python3 manage.py createsuperuser    # MacOS/Linux

* Запустить сервер:

      python manage.py runserver     # Windows
      python3 manage.py runserver    # MacOS/Linux