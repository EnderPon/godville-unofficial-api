class ApiParser:
    # Обработка API (https://godville.net/gods/api/***)
    # Большая часть информации есть на странице героя, за исключением
    # даты сбора пенсии, и максимальных ХП и инвенаря.
    def __init__(self, api_obj):
        self.api = api_obj
        return

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

    def get(self):
        result = {}
        result.update(self.public())
        return result
