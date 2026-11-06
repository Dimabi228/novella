import random
import time


ITEMS = {
    "фонарик": "Фонарик. Помогает в темноте.",
    "ключ1": "Медный ключ с гравировкой I.",
    "ключ2": "Серебряный ключ с гравировкой II.",
    "ключ3": "Чёрный ключ с гравировкой III.",
    "нож": "Ржавый кухонный нож.",
    "записка": "Записка: «Не пиши своё имя».",
    "соль": "Соль. Отпугивает тени.",
    "амулет": "Странный амулет из подвала.",
    "дневник": "Дневник прошлого владельца.",
    "свеча": "Свеча. Освещает путь.",
    "верёвка": "Крепкая верёвка.",
    "зелье": "Зелье. Восстанавливает здоровье.",
    "монета": "Старинная монета для торговца.",
    "чернила": "Чёрные чернила.",
    "перо": "Чёрное перо для тетради.",
    "оберег": "Оберег из соли и верёвки.",
}

ENEMIES = {
    "тень": ("фонарик", "Бесформенная тень у стены."),
    "страж": ("соль", "Каменный страж у двери."),
    "паук": ("нож", "Гигантский паук в подвале."),
    "призрак": ("свеча", "Призрак прошлого владельца."),
    "элиас": ("амулет", "Тот, кто тоже знал о тетради."),
}

RIDDLES = {
    "Что можно записать, но нельзя стереть?": ("имя", "Дают при рождении."),
    "Чем больше берёшь, тем больше становится?": ("яма", "Копают в земле."),
    "Кто умирает, но не живёт?": ("слух", "О нём говорят, когда он проходит."),
    "Что идёт, но не двигается?": ("время", "Его нельзя остановить."),
    "Что принадлежит тебе, но другие используют чаще?": ("имя", "Его произносят вслух."),
}

CRAFT_RECIPES = {
    "оберег": ["соль", "верёвка"],
    "зелье": ["чернила", "свеча"],
}


class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.keys_collected = set()
        self.defeated = set()
        self.completed = set()
        self.hp = 3
        self.max_hp = 3
        self.gold = 2
        self.reputation = 0

    def has(self, item):
        return item in self.inventory

    def take(self, item):
        if item in ITEMS and item not in self.inventory:
            self.inventory.append(item)
            print(f"  [+] Взят: {item} — {ITEMS[item]}")
            return True
        print("  [!] Нет такого предмета.")
        return False

    def remove(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def heal(self, amount=1):
        self.hp = min(self.max_hp, self.hp + amount)
        print(f"  [+] HP: {self.hp}/{self.max_hp}")

    def show_inventory(self):
        if not self.inventory:
            print("  Инвентарь пуст.")
        else:
            print(f"  Инвентарь ({len(self.inventory)}):")
            for i, item in enumerate(self.inventory, 1):
                print(f"    {i}. {item} — {ITEMS[item]}")
        print(f"  HP: {self.hp}/{self.max_hp} | Золото: {self.gold} | Репутация: {self.reputation}")


def slow_print(text, delay=0.02):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def ask(prompt):
    return input(f"\n>> {prompt}: ").strip().lower()


def check_death(player):
    if player.hp <= 0:
        header("ТЫ ПОГИБ")
        slow_print("Тетрадь забирает своё. Твоё имя появляется на странице.")
        slow_print("=== КОНЕЦ ===")
        return True
    return False


def combat(player, enemy_name):
    if enemy_name in player.defeated:
        print(f"  {enemy_name} уже побеждён.")
        return True
    weakness, desc = ENEMIES[enemy_name]
    slow_print(f"Перед тобой {desc}")
    if player.has(weakness):
        slow_print(f"Ты используешь {weakness} — {enemy_name} побеждён.")
        player.defeated.add(enemy_name)
        return True
    slow_print(f"Без {weakness} ты не можешь победить.")
    player.hp -= 1
    print(f"  [-] HP: {player.hp}/{player.max_hp}")
    return not check_death(player)


def try_craft(player):
    print("  Доступные рецепты: оберег (соль+верёвка), зелье (чернила+свеча)")
    choice = ask("Что создать?")
    if choice in CRAFT_RECIPES:
        recipe = CRAFT_RECIPES[choice]
        if all(player.has(i) for i in recipe):
            for i in recipe:
                player.remove(i)
            player.take(choice)
            slow_print(f"Ты создал {choice}.")
        else:
            slow_print(f"Не хватает: {' + '.join(recipe)}")
    else:
        slow_print("Нет такого рецепта.")


def level1(player):
    header("УРОВЕНЬ 1 — КОМНАТА")
    slow_print("Дождь стучит по окнам. Ты в комнате общежития.")
    slow_print("На полу — чёрная тетрадь. Рядом три запертых ящика.")
    slow_print("Найди три ключа, чтобы выйти.")

    actions = [
        "осмотреть комнату",
        "взять фонарик",
        "взять записку",
        "открыть ящик 1",
        "открыть ящик 2",
        "открыть ящик 3",
        "инвентарь",
        "выйти в коридор",
    ]

    boxes = {"ящик 1": "ключ1", "ящик 2": "ключ2", "ящик 3": "ключ3"}
    opened_boxes = set()

    while True:
        print("\nДействия:")
        for i, a in enumerate(actions, 1):
            print(f"  {i}. {a}")

        cmd = ask("Что делаешь?")

        if cmd in ("осмотреть комнату", "осмотреть", "1"):
            slow_print("Фонарик на столе, три ящика, записка в углу.")
        elif cmd in ("взять фонарик", "2"):
            player.take("фонарик")
        elif cmd in ("взять записку", "3"):
            player.take("записка")
        elif cmd in ("открыть ящик 1", "4", "ящик 1"):
            if "ящик 1" in opened_boxes:
                print("  Ящик 1 уже открыт.")
            elif player.has("фонарик"):
                slow_print("Ты светишь фонариком и открываешь ящик 1.")
                player.take(boxes["ящик 1"])
                player.keys_collected.add(boxes["ящик 1"])
                opened_boxes.add("ящик 1")
            else:
                slow_print("Темно. Нужен фонарик.")
                player.hp -= 1
                print(f"  [-] HP: {player.hp}/{player.max_hp}")
                if check_death(player):
                    return False
        elif cmd in ("открыть ящик 2", "5", "ящик 2"):
            if "ящик 2" in opened_boxes:
                print("  Ящик 2 уже открыт.")
            elif player.has("ключ1"):
                slow_print("Ключ 1 подходит. Ящик открыт.")
                player.take(boxes["ящик 2"])
                player.keys_collected.add(boxes["ящик 2"])
                opened_boxes.add("ящик 2")
            else:
                slow_print("Нужен ключ 1.")
        elif cmd in ("открыть ящик 3", "6", "ящик 3"):
            if "ящик 3" in opened_boxes:
                print("  Ящик 3 уже открыт.")
            elif player.has("ключ2"):
                slow_print("Ключ 2 подходит. Ящик открыт.")
                player.take(boxes["ящик 3"])
                player.keys_collected.add(boxes["ящик 3"])
                opened_boxes.add("ящик 3")
            else:
                slow_print("Нужен ключ 2.")
        elif cmd in ("инвентарь", "7"):
            player.show_inventory()
        elif cmd in ("выйти в коридор", "8", "коридор", "выйти"):
            if len(player.keys_collected) >= 3:
                slow_print("Все три ключа собраны. Дверь открывается.")
                player.completed.add("уровень1")
                return True
            print(f"  Нужно 3 ключа. У тебя {len(player.keys_collected)}.")
        else:
            print("  Неизвестная команда.")


def level2(player):
    header("УРОВЕНЬ 2 — КОРИДОР ТЕНЕЙ")
    slow_print("Коридор тянется в темноту. Впереди комнаты и враги.")
    slow_print("Победи тень и стража, чтобы пройти дальше.")

    actions = [
        "осмотреть коридор",
        "идти в подвал",
        "идти в библиотеку",
        "сразиться с тенью",
        "сразиться со стражем",
        "сразиться с пауком",
        "сразиться с призраком",
        "создать предмет",
        "инвентарь",
        "попытаться выйти",
    ]

    while True:
        print("\nДействия:")
        for i, a in enumerate(actions, 1):
            print(f"  {i}. {a}")

        cmd = ask("Что делаешь?")

        if cmd in ("осмотреть коридор", "осмотреть", "1"):
            slow_print("Темно. У стен символы. Слышен шёпот.")
        elif cmd in ("идти в подвал", "2", "подвал"):
            if "паук" not in player.defeated:
                slow_print("Паук преграждает путь!")
            else:
                slow_print("В подвале находишь амулет, дневник и верёвку.")
                player.take("амулет")
                player.take("дневник")
                player.take("верёвка")
        elif cmd in ("идти в библиотеку", "3", "библиотека"):
            if "страж" not in player.defeated:
                slow_print("Страж не пускает!")
            else:
                slow_print("В библиотеке находишь соль, свечу и чернила.")
                player.take("соль")
                player.take("свеча")
                player.take("чернила")
        elif cmd in ("сразиться с тенью", "4", "тень"):
            if not combat(player, "тень"):
                return False
        elif cmd in ("сразиться со стражем", "5", "страж"):
            if not combat(player, "страж"):
                return False
        elif cmd in ("сразиться с пауком", "6", "паук"):
            if not combat(player, "паук"):
                return False
        elif cmd in ("сразиться с призраком", "7", "призрак"):
            if not combat(player, "призрак"):
                return False
        elif cmd in ("создать предмет", "8"):
            try_craft(player)
        elif cmd in ("инвентарь", "9"):
            player.show_inventory()
        elif cmd in ("попытаться выйти", "10", "выйти"):
            if "тень" in player.defeated and "страж" in player.defeated:
                slow_print("Путь свободен.")
                player.completed.add("уровень2")
                return level3(player)
            slow_print("Сначала победи тень и стража.")
        else:
            print("  Неизвестная команда.")


def level3(player):
    header("УРОВЕНЬ 3 — БИБЛИОТЕКА")
    slow_print("В центре библиотеки — стол с тетрадью.")
    slow_print("Элиас ждёт тебя. Разгадай загадки или сразись с ним.")

    actions = [
        "осмотреть библиотеку",
        "поговорить с Элиасом",
        "сразиться с Элиасом",
        "создать предмет",
        "использовать зелье",
        "разгадать загадку",
        "написать имя",
        "инвентарь",
    ]

    while True:
        print("\nДействия:")
        for i, a in enumerate(actions, 1):
            print(f"  {i}. {a}")

        cmd = ask("Что делаешь?")

        if cmd in ("осмотреть библиотеку", "осмотреть", "1"):
            slow_print("Книги шепчут твоё имя. Тетрадь ждёт.")
        elif cmd in ("поговорить с Элиасом", "2", "элиас"):
            slow_print("Элиас: «Тетрадь нельзя уничтожить. Но можно обмануть.»")
            slow_print("Элиас: «Напиши имя с условием — и ты свободен.»")
            player.reputation += 1
        elif cmd in ("сразиться с Элиасом", "3"):
            if not combat(player, "элиас"):
                return False
            slow_print("Элиас побеждён. Тетрадь теперь твоя.")
            return ending_dark(player)
        elif cmd in ("создать предмет", "4"):
            try_craft(player)
        elif cmd in ("использовать зелье", "5"):
            if player.has("зелье"):
                player.remove("зелье")
                player.heal(2)
            else:
                slow_print("У тебя нет зелья.")
        elif cmd in ("разгадать загадку", "6"):
            return final_riddle(player)
        elif cmd in ("написать имя", "7"):
            slow_print("Ты пишешь своё имя с условием: «Умру через 10 лет.»")
            slow_print("Тетрадь принимает. Ты свободен.")
            return ending_freedom(player)
        elif cmd in ("инвентарь", "8"):
            player.show_inventory()
        else:
            print("  Неизвестная команда.")


def final_riddle(player):
    header("ФИНАЛ — ЗАГАДКИ")
    slow_print("Ответь на три загадки.")

    questions = list(RIDDLES.keys())
    random.shuffle(questions)

    correct = 0
    for q in questions[:3]:
        answer, hint = RIDDLES[q]
        slow_print(f"\nЗагадка: {q}")
        slow_print(f"Подсказка: {hint}")
        if ask("Ответ") == answer:
            print("  [+] Верно!")
            correct += 1
        else:
            print(f"  [-] Неверно. Ответ: {answer}")

    if correct >= 2:
        return ending_freedom(player)
    return ending_death(player)


def ending_freedom(player):
    header("ПОБЕДА")
    slow_print("Дверь открывается. Ты выходишь из общежития.")
    slow_print("=== КОНЦОВКА «СВОБОДА» ===")
    return True


def ending_dark(player):
    header("ТЁМНАЯ КОНЦОВКА")
    slow_print("Ты победил Элиаса. Но тетрадь теперь принадлежит тебе.")
    slow_print("=== КОНЦОВКА «БОГ НОВОГО МИРА» ===")
    return True


def ending_death(player):
    header("ПОРАЖЕНИЕ")
    slow_print("Дверь не поддаётся. Тетрадь забирает тебя.")
    slow_print("=== КОНЕЦ ===")
    return False


def main():
    header("ТЕТРАДЬ ТЕНЕЙ")
    slow_print("Текстовая новелла с элементами квеста.")
    slow_print("Собирай предметы, побеждай врагов, разгадывай загадки.")
    slow_print("Вводи команды словами или цифрами.")

    name = input("\nКак тебя зовут? ").strip() or "Артём"
    player = Player(name)

    slow_print(f"\n{player.name}, твоя история начинается...")

    if not level1(player):
        return
    if not level2(player):
        return

    print("\nСпасибо за игру!")


if __name__ == "__main__":
    main()