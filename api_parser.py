class ApiParser:
    # Обработка малого API (https://godville.net/gods/api/***.json)
    # Большая часть информации есть на странице героя, за исключением
    # даты сбора пенсии, и максимальных ХП и инвенаря.
    # Так же тут можно получить оперативные данные, если стоит нужная галочка.
    def __init__(self, api_obj):
        self.update_inv = True  # переделывать инвентарь в массив или оставить как раньше?
        self.api = api_obj
        return

    def inventory(self):
        # Превращаем инвентарь в массив [{},{}]

        inv_len = self.api["inventory_num"]
        old_inv = self.api["inventory"]
        new_inv = []
        for i in range(inv_len):
            new_inv.append(None)
        for name, stats in old_inv.items():
            #print(name, stats)
            item = {"name": name,
                    "cnt": stats["cnt"],
                    "bold": False,
                    "heal_potion": False,
                    "activate_by_user": False,
                    "needs_godpower": 0,
                    "description": ""}

            if "type" in stats:
                item["is_heal_potion"] = True
            if "activate_by_user" in stats:
                item["activate_by_user"] = True
                item["needs_godpower"] = stats["needs_godpower"]
                item["description"] = stats["description"]
            if "type" in stats:
                item["healing"] = True
            if stats["price"] == 101:
                item["bold"] = True
            new_inv[stats["pos"]] = item
        return new_inv

    def pet(self):
        # Если питомец не контужен, то явно это указываем
        if "wounded" not in self.api["pet"]:
            self.api["pet"]["wounded"] = False

    def public(self):
        # максимум хп, инвентаря, дата пенсии
        pub = {"inventory_max_num": self.api["inventory_max_num"],
               "max_health": self.api["max_health"]}
        if "savings_completed_at" in self.api:
            pub["savings_completed_at"] = self.api["savings_completed_at"]
        else:
            pub["savings_completed_at"] = ""
        return pub

    def private(self):
        # Приватная часть АПИ
        # Если ХП нет, то и галочки нет
        priv_api = {}
        if "health" not in self.api:
            return priv_api

        # Добавляем поля ауры, протухания данных и типа боя
        priv_api = {"arena_fight": self.api["arena_fight"],
                    "aura": "",
                    "diary_last": self.api["diary_last"],
                    "distance": self.api["distance"],
                    "exp_progress": self.api["exp_progress"],
                    "expired": False,
                    "fight_type": "",
                    "godpower": self.api["godpower"],
                    "health": self.api["health"],
                    "inventory": self.api["inventory"],
                    "inventory_num": self.api["inventory_num"],
                    "quest_progress": self.api["quest_progress"],
                    "quest": self.api["quest"],
                    "town_name": self.api["town_name"],
                    }
        if "aura" in self.api:
            priv_api["aura"] = self.api["aura"]
        if "expired" in self.api:
            priv_api["expired"] = self.api["expired"]
        if "fight_type" in self.api:
            priv_api["fight_type"] = self.api["fight_type"]

        # Переделаем инвентарь в массив
        if priv_api["inventory_num"] > 0:
            priv_api["inventory"] = self.inventory()
        else:
            priv_api["inventory"] = []

        # Если есть питомец, сделаем поправку
        if "pet" in self.api:
            self.api["pet"] = self.pet()

        return priv_api

    def get(self):
        result = {}
        result.update(self.public())
        result.update(self.private())
        return result
