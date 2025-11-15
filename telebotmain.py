import telebot
from telebot import types
from clases import MobileOperator, Tariff, Subscriber, Bonus

vodafone = MobileOperator("Vodafone")
kyivstar = MobileOperator("Kyivstar")
lifecell = MobileOperator("Lifecell")

operators = {"Vodafone": vodafone, "Kyivstar": kyivstar, "Lifecell": lifecell}

# Демо
SuperNet_Turbo_tariff = Tariff("SuperNet Turbo", 190, 40, 800, 0)
Joice_Pro_tariff = Tariff("Joice Pro", 260, 30, 600, 0)
Joice_Max_tariff = Tariff("Joice Max", 330, 40, 700, 0)
Love_UA_Mahnit_Kontrakt_tariff = Tariff("Love UA Магніт Контракт", 175, 20, 1200, 0)
Potuzhnyi_tariff = Tariff("Потужний", 100, 40, 800, 0)

vodafone.add_tariff(SuperNet_Turbo_tariff)
vodafone.add_tariff(Joice_Pro_tariff)
vodafone.add_tariff(Joice_Max_tariff)
kyivstar.add_tariff(Love_UA_Mahnit_Kontrakt_tariff)
lifecell.add_tariff(Potuzhnyi_tariff)

# Додавання абонентів (10 абонентів)
subscriber1 = Subscriber("Яків", "+380509538984", SuperNet_Turbo_tariff, 200, "Vodafone")
subscriber2 = Subscriber("Денис", "+380509086915", Joice_Pro_tariff, 300, "Vodafone")
subscriber3 = Subscriber("Інна", "+380991760345", Joice_Max_tariff, 500, "Vodafone")
subscriber4 = Subscriber("Ірина", "+380687518196", SuperNet_Turbo_tariff, 100, "Vodafone")
subscriber5 = Subscriber("Марко", "+380997604641", Joice_Pro_tariff, 250, "Vodafone")
subscriber6 = Subscriber("Віталій", "+380667361901", Love_UA_Mahnit_Kontrakt_tariff, 150, "Kyivstar")
subscriber7 = Subscriber("Юлія", "+380681889826", Love_UA_Mahnit_Kontrakt_tariff, 400, "Kyivstar")
subscriber8 = Subscriber("Богдан", "+380985484226", Love_UA_Mahnit_Kontrakt_tariff, 200, "Kyivstar")
subscriber9 = Subscriber("Максим", "+17806606623", Potuzhnyi_tariff, 350, "Lifecell")
subscriber10 = Subscriber("Вікторія", "+380675480970", Potuzhnyi_tariff, 300, "Lifecell")

vodafone.add_subscriber(subscriber1)
vodafone.add_subscriber(subscriber2)
vodafone.add_subscriber(subscriber3)
vodafone.add_subscriber(subscriber4)
vodafone.add_subscriber(subscriber5)
kyivstar.add_subscriber(subscriber6)
kyivstar.add_subscriber(subscriber7)
kyivstar.add_subscriber(subscriber8)
lifecell.add_subscriber(subscriber9)
lifecell.add_subscriber(subscriber10)

# Додавання бонусів (5 бонусів)
bonus1 = Bonus("Чорна п'ятниця", discount=10, extra_internet=10, extra_minutes=0, extra_sms=0)
bonus2 = Bonus("Літня знижка", discount=30, extra_internet=10, extra_minutes=100, extra_sms=20)
bonus3 = Bonus("Весняний подарунок", discount=15, extra_internet=3, extra_minutes=30, extra_sms=5)
bonus4 = Bonus("Зимова знижка", discount=25, extra_internet=7, extra_minutes=70, extra_sms=15)
bonus5 = Bonus("Осінній розпродаж", discount=10, extra_internet=2, extra_minutes=20, extra_sms=5)

vodafone.add_bonus(bonus1)
vodafone.add_bonus(bonus2)
kyivstar.add_bonus(bonus3)
lifecell.add_bonus(bonus4)
lifecell.add_bonus(bonus5)
# Демо

API_TOKEN = '7054122247:AAGgPxpWwbvg-k5emlXQ0rfT-Cmcy4iAmcg' 
bot = telebot.TeleBot(API_TOKEN)

user_states = 0

@bot.message_handler(commands=['start'])
def main_menu(message):
    global user_states
    if user_states == 0:
        bot.send_message(
            message.chat.id,
            "👋 Вітаю! Я бот для управління мобільними операторами. Ось що я вмію:\n"
            "🔹 Додавати, переглядати, редагувати та видаляти інформацію про тарифи, абонентів та бонуси.\n"
            "🔹 Застосовувати бонуси до абонентів.\n"
            "🔹 Показувати актуальну інформацію про операторів.\n"
            "Оберіть дію з меню нижче:",
        )
        user_states =1


    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🌐 Інформація про операторів")
    btn2 = types.KeyboardButton("👁️ Переглянути тарифи")
    btn3 = types.KeyboardButton("👁️ Переглянути абонентів")
    btn4 = types.KeyboardButton("👁️ Переглянути бонуси")
    btn5 = types.KeyboardButton("✅ Застосувати бонус")
    btn6 = types.KeyboardButton("➕ Додати дані")
    btn7 = types.KeyboardButton("🗑️ Видалити елементи")
    btn8 = types.KeyboardButton("✍️ Змінити записи")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    bot.send_message(message.chat.id, "Оберіть дію:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🌐 Інформація про операторів")
def operator_info(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Vodafone 🟥", "Kyivstar 🟦", "Lifecell 🟨", "🔙 Головне меню")
    bot.send_message(message.chat.id, "Оберіть оператора для перегляду інформації:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Vodafone 🟥", "Kyivstar 🟦", "Lifecell 🟨"])
def operator_details(message):
    operator_name = message.text
    info, inline_markup = get_operator_details(operator_name)
    bot.send_message(message.chat.id, info, parse_mode="Markdown", reply_markup=inline_markup)

def get_operator_details(operator_name):
    details = {
        "Vodafone 🟥": {
            "website": "https://www.vodafone.ua",
            "hotline": "0 800 400 111",
            "address": "Київ, вул. Лейпцизька, 15",
            "maps_link": "https://www.google.com/maps?q=Київ,+вул.+Лейпцизька,+15",
            "tariffs_link": "https://www.vodafone.ua/rates#contract",
        },
        "Kyivstar 🟦": {
            "website": "https://www.kyivstar.ua",
            "hotline": "0 800 300 466",
            "address": "м. Київ, вул. Дегтярівська, 53A",
            "maps_link": "https://www.google.com/maps?q=м.+Київ,+вул.+Дегтярівська,+53A",
            "tariffs_link": "https://kyivstar.ua/tariffs",
        },
        "Lifecell 🟨": {
            "website": "https://www.lifecell.ua",
            "hotline": "0 800 20 5433",
            "address": "м. Київ, вул. Солом'янська, 11",
            "maps_link": "https://www.google.com/maps?q=м.+Київ,+вул.+Солом'янська,+11",
            "tariffs_link": "https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/",
        },
    }

    operator_info = details[operator_name]

    info = (
        f"📡 *Інформація про {operator_name}:*\n"
        f"📞 Гаряча лінія: {operator_info['hotline']}\n"
        f"📍 Адреса: {operator_info['address']}\n\n"
        f"📋 *Тарифи:*\n[Переглянути тарифи]({operator_info['tariffs_link']})"
    )

    inline_markup = types.InlineKeyboardMarkup()
    inline_markup.add(
        types.InlineKeyboardButton("📍 Адреса", url=operator_info["maps_link"]),
        types.InlineKeyboardButton("📋 Тарифи", url=operator_info["tariffs_link"]),
        types.InlineKeyboardButton("🔗 Офіційний сайт", url=operator_info["website"])
    )

    return info, inline_markup

@bot.message_handler(func=lambda message: message.text == "🔙 Головне меню")
def go_to_main_menu(message):
    main_menu(message)

@bot.message_handler(func=lambda message: message.text == "➕ Додати дані")
def add_data(message):
    user_id = message.chat.id
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for operator_name in operators.keys():
        markup.add(operator_name)
    markup.add("🔙 Головне меню")
    bot.send_message(user_id, "Оберіть оператора для додавання даних:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in operators.keys())


@bot.message_handler(func=lambda message: message.text in operators.keys() and "перегляду" not in message.text.lower())
def add_data_for_operator(message):
    operator = operators[message.text]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Додати тариф", "Додати абонента", "Додати бонус", "🔙 Головне меню")
    bot.send_message(message.chat.id, f"Оберіть, що додати для {operator.name}:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Додати тариф")
def add_tariff(message):
    operator_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for operator_name in operators.keys():
        operator_markup.add(operator_name)
    bot.send_message(message.chat.id, "Оберіть оператора для додавання тарифу:", reply_markup=operator_markup)
    bot.register_next_step_handler(message, get_operator_for_tariff)

def get_operator_for_tariff(message):
    operator_name = message.text
    if operator_name not in operators.keys():
        bot.send_message(message.chat.id, "Некоректний оператор. Спробуйте ще раз.")
        main_menu(message)
        return
    
    operator = operators[operator_name]
    msg = bot.send_message(message.chat.id, "Введіть назву тарифу:")
    bot.register_next_step_handler(msg, get_tariff_name, operator_name)

def get_tariff_name(message, operator_name):
    tariff_name = message.text
    msg = bot.send_message(message.chat.id, "Введіть ціну тарифу (грн):")
    bot.register_next_step_handler(msg, get_tariff_price, operator_name, tariff_name)

def get_tariff_price(message, operator_name, tariff_name):
    try:
        price = float(message.text)
        msg = bot.send_message(message.chat.id, "Введіть ліміт інтернету (ГБ):")
        bot.register_next_step_handler(msg, get_tariff_internet, operator_name, tariff_name, price)
    except ValueError:
        bot.send_message(message.chat.id, "Ціна повинна бути числом. Спробуйте ще раз.")
        main_menu(message)

def get_tariff_internet(message, operator_name, tariff_name, price):
    try:
        internet_limit = int(message.text)
        msg = bot.send_message(message.chat.id, "Введіть кількість хвилин:")
        bot.register_next_step_handler(msg, get_tariff_minutes, operator_name, tariff_name, price, internet_limit)
    except ValueError:
        bot.send_message(message.chat.id, "Ліміт інтернету повинен бути цілим числом. Спробуйте ще раз.")
        main_menu(message)

def get_tariff_minutes(message, operator_name, tariff_name, price, internet_limit):
    try:
        call_minutes = int(message.text)
        msg = bot.send_message(message.chat.id, "Введіть кількість SMS:")
        bot.register_next_step_handler(msg, save_tariff, operator_name, tariff_name, price, internet_limit, call_minutes)
    except ValueError:
        bot.send_message(message.chat.id, "Кількість хвилин повинна бути цілим числом. Спробуйте ще раз.")
        main_menu(message)

def save_tariff(message, operator_name, tariff_name, price, internet_limit, call_minutes):
    try:
        sms_limit = int(message.text)
        operator = operators[operator_name]
        tariff = Tariff(tariff_name, price, internet_limit, call_minutes, sms_limit)
        operator.add_tariff(tariff)
        bot.send_message(message.chat.id, f"Тариф '{tariff_name}' успішно додано до оператора {operator_name}.")
        main_menu(message)
    except ValueError:
        bot.send_message(message.chat.id, "Кількість SMS повинна бути цілим числом. Спробуйте ще раз.")
        main_menu(message)


@bot.message_handler(func=lambda message: message.text == "Додати абонента")
def add_subscriber(message):
    msg = bot.send_message(message.chat.id, "Введіть ім'я абонента:")
    bot.register_next_step_handler(msg, get_subscriber_name)

def get_subscriber_name(message):
    subscriber_name = message.text
    msg = bot.send_message(message.chat.id, "Введіть номер телефону абонента:")
    bot.register_next_step_handler(msg, get_subscriber_phone, subscriber_name)

def get_subscriber_phone(message, subscriber_name):
    subscriber_phone = message.text
    msg = bot.send_message(message.chat.id, "Введіть баланс абонента (грн):")
    bot.register_next_step_handler(msg, get_subscriber_balance, subscriber_name, subscriber_phone)

def get_subscriber_balance(message, subscriber_name, subscriber_phone):
    try:
        balance = float(message.text)
        operator_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for operator_name in operators.keys():
            operator_markup.add(operator_name)
        bot.send_message(message.chat.id, "Оберіть оператора:", reply_markup=operator_markup)
        bot.register_next_step_handler(message, select_operator_for_subscriber, subscriber_name, subscriber_phone, balance)
    except ValueError:
        bot.send_message(message.chat.id, "Баланс має бути числом. Спробуйте ще раз.")
        main_menu(message)

def select_operator_for_subscriber(message, subscriber_name, subscriber_phone, balance):
    operator_name = message.text
    if operator_name not in operators.keys():
        bot.send_message(message.chat.id, "Некоректний оператор. Спробуйте ще раз.")
        main_menu(message)
        return

    operator = operators[operator_name]
    if not operator.tariffs:
        bot.send_message(message.chat.id, f"У оператора {operator_name} немає тарифів. Спочатку додайте тариф.")
        main_menu(message)
        return

    tariff_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for tariff in operator.tariffs:
        tariff_markup.add(tariff.name)
    bot.send_message(message.chat.id, "Оберіть тариф для абонента:", reply_markup=tariff_markup)
    bot.register_next_step_handler(message, save_subscriber, subscriber_name, subscriber_phone, balance, operator_name)

def save_subscriber(message, subscriber_name, subscriber_phone, balance, operator_name):
    tariff_name = message.text
    operator = operators[operator_name]

    tariff = next((t for t in operator.tariffs if t.name == tariff_name), None)
    if not tariff:
        bot.send_message(message.chat.id, "Тариф не знайдено. Спробуйте ще раз.")
        main_menu(message)
        return

    subscriber = Subscriber(subscriber_name, subscriber_phone, tariff, balance, operator_name)
    operator.add_subscriber(subscriber)
    bot.send_message(message.chat.id, f"Абонента '{subscriber_name}' успішно додано до оператора {operator_name}.")
    main_menu(message)

@bot.message_handler(func=lambda message: message.text == "Додати бонус")
def add_bonus(message):
    msg = bot.send_message(message.chat.id, "Введіть назву бонусу:")
    bot.register_next_step_handler(msg, get_bonus_name)

def get_bonus_name(message):
    bonus_name = message.text
    msg = bot.send_message(message.chat.id, "Введіть знижку (грн):")
    bot.register_next_step_handler(msg, get_bonus_discount, bonus_name)

def get_bonus_discount(message, bonus_name):
    try:
        discount = float(message.text)
        msg = bot.send_message(message.chat.id, "Введіть додатковий інтернет (ГБ):")
        bot.register_next_step_handler(msg, get_bonus_internet, bonus_name, discount)
    except ValueError:
        bot.send_message(message.chat.id, "Знижка має бути числом. Спробуйте ще раз.")
        main_menu(message)

def get_bonus_internet(message, bonus_name, discount):
    try:
        extra_internet = int(message.text)
        msg = bot.send_message(message.chat.id, "Введіть додаткові хвилини:")
        bot.register_next_step_handler(msg, get_bonus_minutes, bonus_name, discount, extra_internet)
    except ValueError:
        bot.send_message(message.chat.id, "Додатковий інтернет має бути цілим числом. Спробуйте ще раз.")
        main_menu(message)

def get_bonus_minutes(message, bonus_name, discount, extra_internet):
    try:
        extra_minutes = int(message.text)
        msg = bot.send_message(message.chat.id, "Введіть додаткові SMS:")
        bot.register_next_step_handler(msg, save_bonus, bonus_name, discount, extra_internet, extra_minutes)
    except ValueError:
        bot.send_message(message.chat.id, "Додаткові хвилини мають бути цілим числом. Спробуйте ще раз.")
        main_menu(message)

def save_bonus(message, bonus_name, discount, extra_internet, extra_minutes):
    try:
        extra_sms = int(message.text)
        operator_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for operator_name in operators.keys():
            operator_markup.add(operator_name)
        msg = bot.send_message(message.chat.id, "Оберіть оператора для додавання бонусу:", reply_markup=operator_markup)
        bot.register_next_step_handler(msg, finalize_bonus, bonus_name, discount, extra_internet, extra_minutes, extra_sms)
    except ValueError:
        bot.send_message(message.chat.id, "Додаткові SMS мають бути цілим числом. Спробуйте ще раз.")
        main_menu(message)

def finalize_bonus(message, bonus_name, discount, extra_internet, extra_minutes, extra_sms):
    operator_name = message.text
    if operator_name not in operators.keys():
        bot.send_message(message.chat.id, "Некоректний оператор. Спробуйте ще раз.")
        main_menu(message)
        return

    operator = operators[operator_name]
    bonus = Bonus(bonus_name, discount, extra_internet, extra_minutes, extra_sms)
    operator.add_bonus(bonus)
    bot.send_message(message.chat.id, f"Бонус '{bonus_name}' успішно додано до оператора {operator_name}.")
    main_menu(message)

@bot.message_handler(func=lambda message: message.text == "👁️ Переглянути тарифи")
def view_all_tariffs(message):
    result = "Тарифи всіх операторів:\n"
    for operator_name, operator in operators.items():
        if operator.tariffs:
            result += f"\nОператор: {operator_name}\n"
            result += "\n".join(
                [f"Назва: {tariff.name}, Ціна: {tariff.price} грн, Інтернет: {tariff.internet_limit} ГБ, "
                 f"Хвилини: {tariff.call_minutes}, SMS: {tariff.sms_limit}" for tariff in operator.tariffs]
            )
        else:
            result += f"\nОператор: {operator_name}\nНемає тарифів.\n"
    bot.send_message(message.chat.id, result)
    go_to_main_menu(message)

@bot.message_handler(func=lambda message: message.text == "👁️ Переглянути абонентів")
def view_all_subscribers(message):
    result = "Абоненти всіх операторів:\n"
    for operator_name, operator in operators.items():
        if operator.subscribers:
            result += f"\nОператор: {operator_name}\n"
            result += "\n".join(
                [f"Ім'я: {sub.name}, Телефон: {sub.phone}, Тариф: {sub.tariff.name}, Баланс: {sub.balance} грн"
                 for sub in operator.subscribers]
            )
        else:
            result += f"\nОператор: {operator_name}\nНемає абонентів.\n"
    bot.send_message(message.chat.id, result)
    go_to_main_menu(message)

@bot.message_handler(func=lambda message: message.text == "👁️ Переглянути бонуси")
def view_all_bonuses(message):
    result = "Бонуси всіх операторів:\n"
    for operator_name, operator in operators.items():
        if operator.bonuses:
            result += f"\nОператор: {operator_name}\n"
            result += "\n".join(
                [f"Назва: {bonus.name}, Знижка: {bonus.discount} грн, Дод. Інтернет: {bonus.extra_internet} ГБ, "
                 f"Дод. Хвилини: {bonus.extra_minutes}, Дод. SMS: {bonus.extra_sms}" for bonus in operator.bonuses]
            )
        else:
            result += f"\nОператор: {operator_name}\nНемає бонусів.\n"
    bot.send_message(message.chat.id, result)
    go_to_main_menu(message)

@bot.message_handler(func=lambda message: message.text == "✅ Застосувати бонус")
def apply_bonus(message):
    operator_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for operator_name in operators.keys():
        operator_markup.add(operator_name)
    bot.send_message(message.chat.id, "Оберіть оператора для застосування бонусу:", reply_markup=operator_markup)
    bot.register_next_step_handler(message, select_operator_for_bonus)

def select_operator_for_bonus(message):
    operator_name = message.text
    if operator_name not in operators.keys():
        bot.send_message(message.chat.id, "Некоректний оператор. Спробуйте ще раз.")
        main_menu(message)
        return

    operator = operators[operator_name]
    if not operator.subscribers:
        bot.send_message(message.chat.id, f"У оператора {operator_name} немає абонентів.")
        main_menu(message)
        return

    subscriber_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for subscriber in operator.subscribers:
        subscriber_markup.add(subscriber.name)
    bot.send_message(message.chat.id, "Оберіть абонента для застосування бонусу:", reply_markup=subscriber_markup)
    bot.register_next_step_handler(message, select_subscriber_for_bonus, operator_name)

def select_subscriber_for_bonus(message, operator_name):
    subscriber_name = message.text
    operator = operators[operator_name]
    subscriber = next((sub for sub in operator.subscribers if sub.name == subscriber_name), None)

    if not subscriber:
        bot.send_message(message.chat.id, "Абонента не знайдено. Спробуйте ще раз.")
        main_menu(message)
        return

    if not operator.bonuses:
        bot.send_message(message.chat.id, f"У оператора {operator_name} немає бонусів.")
        main_menu(message)
        return

    bonus_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for bonus in operator.bonuses:
        bonus_markup.add(bonus.name)
    bot.send_message(message.chat.id, "Оберіть бонус для застосування:", reply_markup=bonus_markup)
    bot.register_next_step_handler(message, apply_selected_bonus, operator_name, subscriber)

def apply_selected_bonus(message, operator_name, subscriber):
    bonus_name = message.text
    operator = operators[operator_name]
    bonus = next((b for b in operator.bonuses if b.name == bonus_name), None)

    if not bonus:
        bot.send_message(message.chat.id, "Бонус не знайдено. Спробуйте ще раз.")
        main_menu(message)
        return

    subscriber.balance += bonus.discount
    subscriber.tariff.internet_limit += bonus.extra_internet
    subscriber.tariff.call_minutes += bonus.extra_minutes
    subscriber.tariff.sms_limit += bonus.extra_sms
    subscriber.tariff.price -= bonus.discount 

    if subscriber.tariff.price < 0:
        subscriber.tariff.price = 0

    bot.send_message(
        message.chat.id,
        f"Бонус '{bonus_name}' успішно застосовано до абонента '{subscriber.name}' оператора {operator_name}.\n"
        f"Оновлена інформація про тариф:\n"
        f"Ціна: {subscriber.tariff.price} грн, Інтернет: {subscriber.tariff.internet_limit} ГБ, "
        f"Хвилини: {subscriber.tariff.call_minutes}, SMS: {subscriber.tariff.sms_limit}"
    )
    main_menu(message)

@bot.message_handler(func=lambda message: message.text == "🗑️ Видалити елементи")
def delete_elements(message):
    operator_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for operator_name in operators.keys():
        operator_markup.add(operator_name)
    operator_markup.add("🔙 Головне меню")
    bot.send_message(message.chat.id, "Оберіть оператора для видалення елементів:", reply_markup=operator_markup)
    bot.register_next_step_handler(message, select_operator_for_deletion)

def select_operator_for_deletion(message):
    operator_name = message.text
    if operator_name not in operators.keys():
        bot.send_message(message.chat.id, "Некоректний оператор. Спробуйте ще раз.")
        main_menu(message)
        return

    operator = operators[operator_name]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Видалити тариф", "Видалити абонента", "Видалити бонус", "🔙 Головне меню")
    bot.send_message(message.chat.id, f"Оберіть, що видалити для оператора {operator.name}:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_deletion_type, operator_name)

def handle_deletion_type(message, operator_name):
    operator = operators[operator_name]
    action = message.text

    if action == "Видалити тариф":
        if not operator.tariffs:
            bot.send_message(message.chat.id, f"У оператора {operator_name} немає тарифів.")
            main_menu(message)
            return

        tariff_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for tariff in operator.tariffs:
            tariff_markup.add(tariff.name)
        tariff_markup.add("🔙 Головне меню")
        bot.send_message(message.chat.id, "Оберіть тариф для видалення:", reply_markup=tariff_markup)
        bot.register_next_step_handler(message, delete_tariff, operator_name)

    elif action == "Видалити абонента":
        if not operator.subscribers:
            bot.send_message(message.chat.id, f"У оператора {operator_name} немає абонентів.")
            main_menu(message)
            return

        subscriber_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for subscriber in operator.subscribers:
            subscriber_markup.add(subscriber.name)
        subscriber_markup.add("🔙 Головне меню")
        bot.send_message(message.chat.id, "Оберіть абонента для видалення:", reply_markup=subscriber_markup)
        bot.register_next_step_handler(message, delete_subscriber, operator_name)

    elif action == "Видалити бонус":
        if not operator.bonuses:
            bot.send_message(message.chat.id, f"У оператора {operator_name} немає бонусів.")
            main_menu(message)
            return

        bonus_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for bonus in operator.bonuses:
            bonus_markup.add(bonus.name)
        bonus_markup.add("🔙 Головне меню")
        bot.send_message(message.chat.id, "Оберіть бонус для видалення:", reply_markup=bonus_markup)
        bot.register_next_step_handler(message, delete_bonus, operator_name)

    else:
        bot.send_message(message.chat.id, "Некоректна дія. Спробуйте ще раз.")
        main_menu(message)

def delete_tariff(message, operator_name):
    tariff_name = message.text
    operator = operators[operator_name]

    tariff = next((t for t in operator.tariffs if t.name == tariff_name), None)
    if not tariff:
        bot.send_message(message.chat.id, "Тариф не знайдено. Спробуйте ще раз.")
        main_menu(message)
        return

    operator.tariffs.remove(tariff)
    bot.send_message(message.chat.id, f"Тариф '{tariff_name}' успішно видалено з оператора {operator_name}.")
    main_menu(message)

def delete_subscriber(message, operator_name):
    subscriber_name = message.text
    operator = operators[operator_name]

    subscriber = next((s for s in operator.subscribers if s.name == subscriber_name), None)
    if not subscriber:
        bot.send_message(message.chat.id, "Абонент не знайдено. Спробуйте ще раз.")
        main_menu(message)
        return

    operator.subscribers.remove(subscriber)
    bot.send_message(message.chat.id, f"Абонент '{subscriber_name}' успішно видалено з оператора {operator_name}.")
    main_menu(message)

def delete_bonus(message, operator_name):
    bonus_name = message.text
    operator = operators[operator_name]

    bonus = next((b for b in operator.bonuses if b.name == bonus_name), None)
    if not bonus:
        bot.send_message(message.chat.id, "Бонус не знайдено. Спробуйте ще раз.")
        main_menu(message)
        return

    operator.bonuses.remove(bonus)
    bot.send_message(message.chat.id, f"Бонус '{bonus_name}' успішно видалено з оператора {operator_name}.")
    main_menu(message)

@bot.message_handler(func=lambda message: message.text == "✍️ Змінити записи")
def modify_records(message):
    operator_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for operator_name in operators.keys():
        operator_markup.add(operator_name)
    operator_markup.add("🔙 Головне меню")
    bot.send_message(message.chat.id, "Оберіть оператора для зміни записів:", reply_markup=operator_markup)
    bot.register_next_step_handler(message, select_operator_for_modification)

def select_operator_for_modification(message):
    operator_name = message.text
    if operator_name not in operators.keys():
        bot.send_message(message.chat.id, "Некоректний оператор. Спробуйте ще раз.")
        main_menu(message)
        return

    operator = operators[operator_name]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Змінити тариф", "Змінити абонента", "Змінити бонус", "🔙 Головне меню")
    bot.send_message(message.chat.id, f"Оберіть, що змінити для оператора {operator.name}:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_modification_type, operator_name)

def handle_modification_type(message, operator_name):
    operator = operators[operator_name]
    action = message.text

    if action == "Змінити тариф":
        if not operator.tariffs:
            bot.send_message(message.chat.id, f"У оператора {operator_name} немає тарифів.")
            main_menu(message)
            return

        tariff_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for tariff in operator.tariffs:
            tariff_markup.add(tariff.name)
        tariff_markup.add("🔙 Головне меню")
        bot.send_message(message.chat.id, "Оберіть тариф для зміни:", reply_markup=tariff_markup)
        bot.register_next_step_handler(message, modify_tariff, operator_name)

    elif action == "Змінити абонента":
        if not operator.subscribers:
            bot.send_message(message.chat.id, f"У оператора {operator_name} немає абонентів.")
            main_menu(message)
            return

        subscriber_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for subscriber in operator.subscribers:
            subscriber_markup.add(subscriber.name)
        subscriber_markup.add("🔙 Головне меню")
        bot.send_message(message.chat.id, "Оберіть абонента для зміни:", reply_markup=subscriber_markup)
        bot.register_next_step_handler(message, modify_subscriber, operator_name)

    elif action == "Змінити бонус":
        if not operator.bonuses:
            bot.send_message(message.chat.id, f"У оператора {operator_name} немає бонусів.")
            main_menu(message)
            return

        bonus_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for bonus in operator.bonuses:
            bonus_markup.add(bonus.name)
        bonus_markup.add("🔙 Головне меню")
        bot.send_message(message.chat.id, "Оберіть бонус для зміни:", reply_markup=bonus_markup)
        bot.register_next_step_handler(message, modify_bonus, operator_name)

    else:
        bot.send_message(message.chat.id, "Некоректна дія. Спробуйте ще раз.")
        main_menu(message)

def modify_tariff(message, operator_name):
    tariff_name = message.text
    operator = operators[operator_name]
    tariff = next((t for t in operator.tariffs if t.name == tariff_name), None)

    if not tariff:
        bot.send_message(message.chat.id, "Тариф не знайдено. Спробуйте ще раз.")
        main_menu(message)
        return

    msg = bot.send_message(message.chat.id, "Введіть нову ціну тарифу (грн):")
    bot.register_next_step_handler(msg, update_tariff_price, operator_name, tariff)

def update_tariff_price(message, operator_name, tariff):
    try:
        tariff.price = float(message.text)
        msg = bot.send_message(message.chat.id, "Введіть новий ліміт інтернету (ГБ):")
        bot.register_next_step_handler(msg, update_tariff_internet, operator_name, tariff)
    except ValueError:
        bot.send_message(message.chat.id, "Ціна повинна бути числом. Спробуйте ще раз.")
        main_menu(message)

def update_tariff_internet(message, operator_name, tariff):
    try:
        tariff.internet_limit = int(message.text)
        msg = bot.send_message(message.chat.id, "Введіть нову кількість хвилин:")
        bot.register_next_step_handler(msg, update_tariff_minutes, operator_name, tariff)
    except ValueError:
        bot.send_message(message.chat.id, "Ліміт інтернету повинен бути цілим числом. Спробуйте ще раз.")
        main_menu(message)

def update_tariff_minutes(message, operator_name, tariff):
    try:
        tariff.call_minutes = int(message.text)
        msg = bot.send_message(message.chat.id, "Введіть нову кількість SMS:")
        bot.register_next_step_handler(msg, finalize_tariff_update, operator_name, tariff)
    except ValueError:
        bot.send_message(message.chat.id, "Кількість хвилин повинна бути цілим числом. Спробуйте ще раз.")
        main_menu(message)

def finalize_tariff_update(message, operator_name, tariff):
    try:
        tariff.sms_limit = int(message.text)
        bot.send_message(message.chat.id, f"Тариф '{tariff.name}' успішно оновлено для оператора {operator_name}.")
        main_menu(message)
    except ValueError:
        bot.send_message(message.chat.id, "Кількість SMS повинна бути цілим числом. Спробуйте ще раз.")
        main_menu(message)

def modify_subscriber(message, operator_name):
    subscriber_name = message.text
    operator = operators[operator_name]
    subscriber = next((s for s in operator.subscribers if s.name == subscriber_name), None)

    if not subscriber:
        bot.send_message(message.chat.id, "Абонент не знайдено. Спробуйте ще раз.")
        main_menu(message)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Змінити баланс", "Змінити тариф", "🔙 Головне меню")
    bot.send_message(message.chat.id, f"Оберіть дію для абонента '{subscriber.name}':", reply_markup=markup)
    bot.register_next_step_handler(message, handle_subscriber_modification, operator_name, subscriber)
def update_subscriber_balance(message, operator_name, subscriber):
    try:
        subscriber.balance = float(message.text)
        bot.send_message(message.chat.id, f"Баланс абонента '{subscriber.name}' успішно змінено на {subscriber.balance} грн.")
        main_menu(message)
    except ValueError:
        bot.send_message(message.chat.id, "Баланс повинен бути числом. Спробуйте ще раз.")
        main_menu(message)

def handle_subscriber_modification(message, operator_name, subscriber):
    action = message.text

    if action == "Змінити баланс":
        msg = bot.send_message(message.chat.id, "Введіть новий баланс абонента (грн):")
        bot.register_next_step_handler(msg, update_subscriber_balance, operator_name, subscriber)
    elif action == "Змінити тариф":
        operator = operators[operator_name]
        if not operator.tariffs:
            bot.send_message(message.chat.id, f"У оператора {operator_name} немає тарифів.")
            main_menu(message)
            return

        tariff_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for tariff in operator.tariffs:
            tariff_markup.add(tariff.name)
        tariff_markup.add("🔙 Головне меню")
        bot.send_message(message.chat.id, "Оберіть новий тариф для абонента:", reply_markup=tariff_markup)
        bot.register_next_step_handler(message, update_subscriber_tariff, operator_name, subscriber)
    else:
        bot.send_message(message.chat.id, "Некоректна дія. Спробуйте ще раз.")
        main_menu(message)

def update_subscriber_tariff(message, operator_name, subscriber):
    tariff_name = message.text
    operator = operators[operator_name]
    tariff = next((t for t in operator.tariffs if t.name == tariff_name), None)

    if not tariff:
        bot.send_message(message.chat.id, "Тариф не знайдено. Спробуйте ще раз.")
        main_menu(message)
        return

    subscriber.tariff = tariff
    bot.send_message(message.chat.id, f"Тариф для абонента '{subscriber.name}' успішно змінено на '{tariff.name}'.")
    main_menu(message)

def modify_bonus(message, operator_name):
    bonus_name = message.text
    operator = operators[operator_name]
    bonus = next((b for b in operator.bonuses if b.name == bonus_name), None)

    if not bonus:
        bot.send_message(message.chat.id, "Бонус не знайдено. Спробуйте ще раз.")
        main_menu(message)
        return

    msg = bot.send_message(message.chat.id, "Введіть нову знижку (грн):")
    bot.register_next_step_handler(msg, update_bonus_discount, operator_name, bonus)

def update_bonus_discount(message, operator_name, bonus):
    try:
        bonus.discount = float(message.text)
        msg = bot.send_message(message.chat.id, "Введіть новий додатковий інтернет (ГБ):")
        bot.register_next_step_handler(msg, update_bonus_internet, operator_name, bonus)
    except ValueError:
        bot.send_message(message.chat.id, "Знижка повинна бути числом. Спробуйте ще раз.")
        main_menu(message)

def update_bonus_internet(message, operator_name, bonus):
    try:
        bonus.extra_internet = int(message.text)
        msg = bot.send_message(message.chat.id, "Введіть нову кількість хвилин:")
        bot.register_next_step_handler(msg, update_bonus_minutes, operator_name, bonus)
    except ValueError:
        bot.send_message(message.chat.id, "Додатковий інтернет повинен бути цілим числом. Спробуйте ще раз.")
        main_menu(message)

def update_bonus_minutes(message, operator_name, bonus):
    try:
        bonus.extra_minutes = int(message.text)
        msg = bot.send_message(message.chat.id, "Введіть нову кількість SMS:")
        bot.register_next_step_handler(msg, finalize_bonus_update, operator_name, bonus)
    except ValueError:
        bot.send_message(message.chat.id, "Додаткові хвилини повинні бути цілим числом. Спробуйте ще раз.")
        main_menu(message)

def finalize_bonus_update(message, operator_name, bonus):
    try:
        bonus.extra_sms = int(message.text)
        bot.send_message(message.chat.id, f"Бонус '{bonus.name}' успішно оновлено для оператора {operator_name}.")
        main_menu(message)
    except ValueError:
        bot.send_message(message.chat.id, "Кількість SMS повинна бути цілим числом. Спробуйте ще раз.")
        main_menu(message)

bot.polling(non_stop=True)