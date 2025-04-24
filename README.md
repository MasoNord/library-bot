# Library Bot
Сервис для поиска кнги по библиотекам города  по названию, автору и году выпуска. Так же там будет напоминание о том, какие книги вы уже взяли и должны в библиотеке. И подборка интересных новинок на основе тех книг, которые искал пользователь

# Технологии
- aiogram
- beautifulsoup4
- requests
- python-dotenv

# Структура проектa

```
project
│
├── bot/
│   ├── handlers.py
│   ├── services.py
│   ├── bot.py
│   ├── config.py
├── .env
├── README.md
├── requirements.txt
├── 2 скриншота.docx
├── вебух deleted.txt
```

# Установка
1. Клонировать репозиторий по следующуей ссылке:
```
https://github.com/MasoNord/library-bot.git
```
2. Перейти в директорию проекта libary-bot:
```
cd libary-bot
```
3. Создать и активировать виртуальное окружение:
```
python -m venv venv

# Для Linux
source venv/bin/activate

# Для Windows
venv\Scriptcs\activate
```

4. Установить необходимые зависимости через следующую команду:
```
pip install -r requirements.txt
```

5. Создать файл `.env` в корне проекта:
```
# Bot Configuration
API_TOKEN=<Your Bot Token>
```

6. Получить токен бота через @BotFather и вставить его в `.env`

7. Запустить бота, для этого выполняем команду с корневой папки:
```
cd bot
python -m bot
```

