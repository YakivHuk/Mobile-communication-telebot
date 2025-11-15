class Tariff:
    def __init__(self, name, price, internet_limit, call_minutes, sms_limit):
        self.name = name
        self.price = price
        self.internet_limit = internet_limit
        self.call_minutes = call_minutes
        self.sms_limit = sms_limit
     
    def edit(self, price=None, internet_limit=None, call_minutes=None, sms_limit=None):
        if price is not None:
            self.price = price
        if internet_limit is not None:
            self.internet_limit = internet_limit
        if call_minutes is not None:
            self.call_minutes = call_minutes
        if sms_limit is not None:
            self.sms_limit = sms_limit

    def print_info(self):
        print(f"Тариф: {self.name}, Ціна: {self.price} грн, Інтернет: {self.internet_limit} ГБ, "
              f"Хвилини: {self.call_minutes} хв, SMS: {self.sms_limit}")

class Subscriber:
    def __init__(self, name, phone, tariff, balance, operator):
        self.name = name
        self.phone = phone
        self.tariff = tariff
        self.balance = balance
        self.operator = operator

    def add_balance(self, amount):
        self.balance += amount
        print(f"{self.name} поповнив баланс на {amount} грн. Новий баланс: {self.balance} грн.")

    def print_info(self):
        print(f"Абонент: {self.name}, Телефон: {self.phone}, Оператор: {self.operator}, "
              f"Тариф: {self.tariff.name}, Баланс: {self.balance} грн.")
        
class Bonus:
    def __init__(self, name, discount=0, extra_internet=0, extra_minutes=0, extra_sms=0):
        self.name = name
        self.discount = discount
        self.extra_internet = extra_internet
        self.extra_minutes = extra_minutes
        self.extra_sms = extra_sms

    def edit_bonus(self, discount=None, extra_internet=None, extra_minutes=None, extra_sms=None):
        if discount is not None:
            self.discount = discount
        if extra_internet is not None:
            self.extra_internet = extra_internet
        if extra_minutes is not None:
            self.extra_minutes = extra_minutes
        if extra_sms is not None:
            self.extra_sms = extra_sms

    def apply_to_tariff(self, subscriber):
        subscriber.tariff.price -= self.discount
        subscriber.tariff.internet_limit += self.extra_internet
        subscriber.tariff.call_minutes += self.extra_minutes
        subscriber.tariff.sms_limit += self.extra_sms
        print(f"Бонус '{self.name}' застосовано до абонента {subscriber.name}.")



class MobileOperator:
    def __init__(self, name):
        self.name = name
        self.tariffs = []
        self.subscribers = []
        self.bonuses = []

    def add_tariff(self, tariff):
        self.tariffs.append(tariff)
        print(f"Тариф '{tariff.name}' додано до оператора {self.name}.")

    def remove_tariff(self, tariff_name):
        for tariff in self.tariffs:
            if tariff.name == tariff_name:
                self.tariffs.remove(tariff)
                print(f"Тариф '{tariff_name}' видалено.")
                return
        print(f"Тариф '{tariff_name}' не знайдено.")

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)
        print(f"Абонента '{subscriber.name}' зареєстровано у {self.name}.")

    def add_bonus(self, bonus):
        self.bonuses.append(bonus)
        print(f"Бонус '{bonus.name}' додано.")

    def remove_bonus(self, bonus_name):
        for bonus in self.bonuses:
            if bonus.name == bonus_name:
                self.bonuses.remove(bonus)
                print(f"Бонус '{bonus_name}' видалено.")
                return
        print(f"Бонус '{bonus_name}' не знайдено.")

    def remove_subscriber(self, phone):
        for subscriber in self.subscribers:
            if subscriber.phone == phone:
                self.subscribers.remove(subscriber)
                print(f"Абонента з номером телефону '{phone}' видалено.")
                return
        print(f"Абонента з номером телефону '{phone}' не знайдено.")

    def save_to_file(self, file_name):
        with open(file_name, mode='w') as f:
            # Збереження тарифів
            f.write("=== Тарифи ===\n")
            f.write(f"{'Назва тарифу':<20} {'Ціна (грн)':<10} {'Інтернет (ГБ)':<15} {'Хвилини':<10} {'SMS':<10}\n")
            f.write("=" * 70 + "\n")
            for tariff in self.tariffs:
                f.write(f"{tariff.name:<20} {tariff.price:<10.2f} {tariff.internet_limit:<15} "
                        f"{tariff.call_minutes:<10} {tariff.sms_limit:<10}\n")
            f.write("\n")

            # Збереження абонентів
            f.write("=== Абоненти ===\n")
            f.write("{:<15} {:<15} {:<10} {:<15} {:<10}\n".format("Ім'я", "Телефон", "Оператор", "Тариф", "Баланс (грн)"))
            f.write("=" * 70 + "\n")
            for subscriber in self.subscribers:
                f.write(f"{subscriber.name:<15} {subscriber.phone:<15} {subscriber.operator:<10} "
                        f"{subscriber.tariff.name:<15} {subscriber.balance:<10.2f}\n")
            f.write("\n")

            # Збереження бонусів
            f.write("=== Бонуси ===\n")
            f.write(f"{'Назва бонусу':<20} {'Знижка (грн)':<15} {'Інтернет (ГБ)':<15} {'Хвилини':<10} {'SMS':<10}\n")
            f.write("=" * 70 + "\n")
            for bonus in self.bonuses:
                f.write(f"{bonus.name:<20} {bonus.discount:<15.2f} {bonus.extra_internet:<15} "
                        f"{bonus.extra_minutes:<10} {bonus.extra_sms:<10}\n")
        print(f"Дані оператора {self.name} збережено у файл '{file_name}'.")


    def print_tariffs(self):
        print(f"\nТарифи оператора {self.name}:")
        print(f"{'Назва тарифу':<20} {'Ціна (грн)':<10} {'Інтернет (ГБ)':<15} {'Хвилини':<10} {'SMS':<10}")
        print("=" * 65)
        for tariff in self.tariffs:
            print(f"{tariff.name:<20} {tariff.price:<10} {tariff.internet_limit:<15} "
                  f"{tariff.call_minutes:<10} {tariff.sms_limit:<10}")
        print("=" * 65)

    def print_subscribers(self):
        print(f"\nАбоненти оператора {self.name}:")
        print(f"{\"Ім'я\":<15} {'Телефон':<15} {'Оператор':<10} {'Тариф':<15} {'Баланс (грн)':<10}")
        print("=" * 65)
        for subscriber in self.subscribers:
            print(f"{subscriber.name:<15} {subscriber.phone:<15} {subscriber.operator:<10} "
                  f"{subscriber.tariff.name:<15} {subscriber.balance:<10.2f}")
        print("=" * 65)

    def print_bonuses(self):
        if not self.bonuses:
            print("\nСписок бонусів порожній.")
            return
        print(f"\nСписок бонусів:")
        print(f"{'Назва бонусу':<20} {'Знижка (грн)':<15} {'Інтернет (ГБ)':<15} {'Хвилини':<10} {'SMS':<10}")
        print("=" * 65)
        for bonus in self.bonuses:
            print(f"{bonus.name:<20} {bonus.discount:<15} {bonus.extra_internet:<15} "
                  f"{bonus.extra_minutes:<10} {bonus.extra_sms:<10}")
        print("=" * 65)



vodafone = MobileOperator("Vodafone")
kyivstar = MobileOperator("Kyivstar")
lifecell = MobileOperator("Lifecell")

# Додавання тарифів 5 тарифів
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
bonus2 = Bonus("Літнія знижка", discount=30, extra_internet=10, extra_minutes=100, extra_sms=20)
bonus3 = Bonus("Весняний подарунок", discount=15, extra_internet=3, extra_minutes=30, extra_sms=5)
bonus4 = Bonus("Зимова знижка", discount=25, extra_internet=7, extra_minutes=70, extra_sms=15)
bonus5 = Bonus("Осінній розпродаж", discount=10, extra_internet=2, extra_minutes=20, extra_sms=5)

vodafone.add_bonus(bonus1)
vodafone.add_bonus(bonus2)
kyivstar.add_bonus(bonus3)
lifecell.add_bonus(bonus4)
lifecell.add_bonus(bonus5)

# Застосування бонусів
bonus1.apply_to_tariff(subscriber1)
bonus2.apply_to_tariff(subscriber2)
bonus3.apply_to_tariff(subscriber6)
bonus4.apply_to_tariff(subscriber9)
bonus5.apply_to_tariff(subscriber10)

# Видалення тарифу
vodafone.remove_tariff("Joice Pro")

# Видалення абонента
vodafone.remove_subscriber("+380675480970")

# Видалення бонусу
kyivstar.remove_bonus("Весняний подарунок")

# Зміна тарифу
SuperNet_Turbo_tariff.edit(price=180, internet_limit=35, call_minutes=900, sms_limit=60)

# Поповнення балансу
subscriber1.add_balance(100)

# Збереження даних у файли
vodafone.save_to_file("vodafone_data.txt")
kyivstar.save_to_file("kyivstar_data.txt")
lifecell.save_to_file("lifecell_data.txt")

# Виведення інформації
vodafone.print_tariffs()
vodafone.print_subscribers()
vodafone.print_bonuses()

kyivstar.print_tariffs()
kyivstar.print_subscribers()
kyivstar.print_bonuses()

lifecell.print_tariffs()
lifecell.print_subscribers()
lifecell.print_bonuses()


