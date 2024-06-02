import telebot
import sqlite3

from telebot import types

global gen
global oce
bot = telebot.TeleBot('5963364766:AAEE-xg3izVBIu6-tZyJPyjMZvIMLXm6fXg')


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}  {message.from_user.last_name}\n'
                                      f'Вот список моих функций:\n '
                                      f'/stop_games - Подборка игр по жанрам и оценкам редакции с 2010 года\n '
                                      f' \n'
                                      f'/playlist - Небольшая подборка музыки от автора)\n'
                                      f' \n '
                                      f'/help - Подсказка с командами')


@bot.message_handler(commands=['stop_games'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Экшн')
    btn2 = types.KeyboardButton('Дополнения')
    btn3 = types.KeyboardButton('Приключения')
    btn4 = types.KeyboardButton('Аркады')
    btn5 = types.KeyboardButton('Карточные')
    btn6 = types.KeyboardButton('Казуальные')
    btn7 = types.KeyboardButton('Обучающие')
    btn8 = types.KeyboardButton('Файтинги')
    btn9 = types.KeyboardButton('Для детей')
    btn10 = types.KeyboardButton('Головоломки')
    btn11 = types.KeyboardButton('ММО')
    btn12 = types.KeyboardButton('Онлайн')
    btn13 = types.KeyboardButton('Гонки')
    btn14 = types.KeyboardButton('РПГ')
    btn15 = types.KeyboardButton('Симуляторы')
    btn16 = types.KeyboardButton('Спортивные')
    btn17 = types.KeyboardButton('Стратегии')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5, btn6)
    markup.row(btn7, btn8)
    markup.row(btn9, btn10)
    markup.row(btn11, btn12)
    markup.row(btn13, btn14)
    markup.row(btn15, btn16, btn17)
    bot.reply_to(message, 'Нажми на интересующий тебя жанр:', reply_markup=markup)

    bot.register_next_step_handler(message, on_click)


def on_click(message):
    global gen
    if message.text == 'Экшн':
        gen = 'action'
        genre_game(message)
    elif message.text == 'Дополнения':
        gen = 'add-on'
        genre_game(message)
    elif message.text == 'Приключения':
        gen = 'adventure'
        genre_game(message)
    elif message.text == 'Аркады':
        gen = 'arcade'
        genre_game(message)
    elif message.text == 'Карточные':
        gen = 'cards'
        genre_game(message)
    elif message.text == 'Казуальные':
        gen = 'casual'
        genre_game(message)
    elif message.text == 'Обучающие':
        gen = 'educational'
        genre_game(message)
    elif message.text == 'Файтинги':
        gen = 'fighting'
        genre_game(message)
    elif message.text == 'Для детей':
        gen = 'for-kids'
        genre_game(message)
    elif message.text == 'Головоломки':
        gen = 'logic'
        genre_game(message)
    elif message.text == 'ММО':
        gen = 'massively multiplayer'
        genre_game(message)
    elif message.text == 'Онлайн':
        gen = 'online'
        genre_game(message)
    elif message.text == 'Гонки':
        gen = 'racing'
        genre_game(message)
    elif message.text == 'РПГ':
        gen = 'rpg'
        genre_game(message)
    elif message.text == 'Симуляторы':
        gen = 'simulator'
        genre_game(message)
    elif message.text == 'Спортивные':
        gen = 'sport'
        genre_game(message)
    elif message.text == 'Стратегии':
        gen = 'strategy'
        genre_game(message)


def genre_game(message):
    markup = types.ReplyKeyboardMarkup()

    btn2 = types.KeyboardButton('5 - Изумительно')
    btn3 = types.KeyboardButton('15 - Изумительно')
    btn5 = types.KeyboardButton('5 - Похвально')
    btn6 = types.KeyboardButton('15 - Похвально')
    btn8 = types.KeyboardButton('5 - Проходняк')
    btn9 = types.KeyboardButton('15 - Проходняк')
    btn11 = types.KeyboardButton('5 - Мусор')
    btn12 = types.KeyboardButton('15 - Мусор')
    markup.row(btn2, btn3)
    markup.row(btn5, btn6)
    markup.row(btn8, btn9)
    markup.row(btn11, btn12)
    bot.reply_to(message, 'Нажми на подходящее ограничение по количеству записей:', reply_markup=markup)
    bot.register_next_step_handler(message, ono_click)


def ono_click(message):
    global oce

    limit = int(message.text.split(' ')[0])
    if message.text.endswith('Изумительно'):
        oce = 'izumitelno'
        vyvod_games(message, limit)
    elif message.text.endswith('Похвально'):
        oce = 'pohvalno'
        vyvod_games(message, limit)
    elif message.text.endswith('Проходняк'):
        oce = 'prohodnyak'
        vyvod_games(message, limit)
    elif message.text.endswith('Мусор'):
        oce = 'musor'
        vyvod_games(message, limit)


def vyvod_games(message, limit):
    global gen
    global oce
    conn = sqlite3.connect('C:\Стафыч\УЧЕБА\ДОП. КУРСЫ\АНАЛИТИКА ДАННЫХ/games8.sql')
    cursor = conn.execute(
        f'''SELECT name, mark, link FROM games WHERE genre = '{gen}' AND ocenka_redaction = '{oce}' ORDER BY mark DESC LIMIT {limit}'''
    )  # Выполнить запрос на выборку всех строк из таблицы
    table_data = cursor.fetchall()  # Получить все данные из таблицы

    for row in table_data:  # Отобразить каждую строку из таблицы
        bot.send_message(message.chat.id, f"{row[0]} ({row[1]}) - {row[2]}")
    conn.commit()

    conn.close()


@bot.message_handler(commands=['playlist'])
def music(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Chill LoFi',
                                      url='https://www.youtube.com/watch?v=dLmyp3xMsAo&list=PLmNdDWjAyYABTPJFeP89nK6lFDIHGY1WQ&index=11')
    btn2 = types.InlineKeyboardButton('Motivation',  url='https://www.youtube.com/watch?v=JLeXAca0hLQ')
    btn3 = types.InlineKeyboardButton('Phonk', url='https://www.youtube.com/watch?v=PEvFuJ2FKHA')
    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    bot.reply_to(message, 'Небольшая подборка от автора', reply_markup=markup)


@bot.message_handler(commands=['help'])
def start_bot(message):
    bot.send_message(message.chat.id, f'Вот список моих функций:\n '
                                      f'/stop_games - Подборка игр по жанрам и оценкам редакции с 2010 года\n '
                                      f' \n'
                                      f'Если после использования команды stop_game, вы хотите посмотреть игры других жанров и оценок, то команду нужно запустить заново\n'
                                      f'\n'
                                      f'/playlist - Небольшая подборка музыки от автора)')


bot.polling(none_stop=True)
