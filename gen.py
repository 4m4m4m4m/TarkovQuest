from faker import Faker
import random

QUEST_TYPES = [
    {
        "name": "Охотник за головами",
        "template": "Убейте {count} {enemy} на локации {location} с {weapon}"
    },
    {
        "name": "Сборщик",
        "template": "Найдите {count} предмета {item} на локации {location}"
    },
    # надо добавить ещё
]

LOCATIONS = ["Таможня", "Завод", "Лес", "Развязка", "Берег"]
ITEMS = ["гайки", "болты", "аптечки", "патроны"]
WEAPONS = ["пистолетом", "дробовиком", "винтовкой"]
ENEMIES = ["Дикий", "ЧВК"]

def generate_random_quest():
    quest_type = random.choice(QUEST_TYPES)
    location = random.choice(LOCATIONS)
    if "item" in quest_type["template"]:
        item = random.choice(ITEMS)
        count = random.randint(1,5)
        text = quest_type["template"].format(count=count, item=item, location=location)
    else:
        weapon = random.choice(WEAPONS)
        count = random.randint(1,10)
        enemy = random.choice(ENEMIES)
        location = random.choice(LOCATIONS)
        text = quest_type["template"].format(count=count, weapon=weapon, enemy=enemy, location=location)
    name = quest_type["name"]
    print("Generated new quest")
    print(name)
    print(text)
    print
    return name, text