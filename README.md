# diabetFoundVolunteersBot
Chatbot to select candidates for volunteering at the Diabetes Foundation.

Чат-бот для набора волонтеров для Фонда Борьбы с Диабетом.

## Развертывание
### Токен и пароль
* Токен телеграм бота должен лежать в файле token.txt
* md5-хэш пароля администратора записывается в bot_main.py. По умолчанию, установлен пароль `admin1337`, соответственно записано `admin_password_hash = '44fe45de0bee447b6a9101036c54b81b'` (строчка после `=` это md5 хэш от `admin1337`)
### Установка и запуск:
```
git clone https://github.com/rgimad/diabetFoundVolunteersBot.git
cd diabetFoundVolunteersBot
python -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
python create_db.py # Создание БД
python bot_main.py # Запуск бота
```


