import re

from bs4 import BeautifulSoup


class GodPageParser:
    # Парсер страницы бога (https://godville.net/gods/***)
    def __init__(self, page_text):
        # фиксим потеряные теги
        page_text = re.sub("""(<td class="label">Сбережения</td>\s*<td class="name">.*?</td>)""",
                           """<tr>\g<1></tr>""", page_text)
        self.soup = BeautifulSoup(page_text, 'html.parser')
        return

    def _clear_name(self, string):
        string_t = str(string)[4:].strip()
        answer = ""
        for i in string_t:
            if i != "\n":
                answer += i
            else:
                answer = answer.strip()
                break
        return answer

    def _str_to_num(self, str_):
        if str_ == "ни одного":
            return 0
        elif str_ == "десяток":
            return 10
        elif str_ == "около сотни":
            return 100
        elif str_ == "около тысячи":
            return 1000
        else:
            try:
                num, line = re.findall("около (\d+) (сотен|тысяч)", str_)[0]
            except:
                print("Unexpected number " + str_)
                return 0
            if line == "тысяч":
                return 1000 * int(num)
            if line == "сотен":
                return 100 * int(num)
            return 0  # сюда не должны попадать

    def get_levels(self):
        levels_str = str(self.soup.find(class_="level").text)
        hero_lvl, trader_lvl = (re.search("(\d+)\D+(\d*)", levels_str).group(1, 2))
        # Хотя бы одна цифра, хотя бы одна не цифра, сколько угодно цифр
        if trader_lvl == "":
            trader_lvl = 0
        hero_lvl = int(hero_lvl)
        trader_lvl = int(trader_lvl)
        return {"hero_lvl": hero_lvl,
                "trader_lvl": trader_lvl}

    def get_essential(self):
        hero = str(self.soup.find(id="essential_info").h3).replace("\n", "")
        hero = re.findall("""<h3>\s*(.*?)<""", hero)[0].strip()
        god = self.soup.find(id="god").h2.text.strip()
        if self.soup.find(class_="caption").text.strip() == "Герой":
            h_gender = "m"
        else:
            h_gender = "f"

        if self.soup.find(id="god").p.text.strip() == "Бог":
            g_gender = "m"
        else:
            g_gender = "f"

        avatar_url = "https://secure.gravatar.com/avatar/" + \
                     str(self.soup.find(id="avatar").img)[10:42]
        motto = self.soup.find(class_="motto").text.strip()

        return {"hero_name": hero,
                "hero_gender": h_gender,
                "god_name": god,
                "god_gender": g_gender,
                "avatar_url": avatar_url,
                "motto": motto}

    def get_badges(self):
        badges_list = {
            "Храмовладелец": "temple",
            "Корабел": "ark",
            "Зверовод": "pet",
            "Тваревед": "creatures"
        }
        result = {
            "temple": None,
            "ark": None,
            "pet": None,
            "creatures": None
        }
        badges_re = re.compile("""<span.*>(.)</span><span.*>(\w*) [сc] ([\d:\. ]*)</span>""")
        if self.soup.find(class_="t_award_d") is None:
            return {"badges": result}
        badges_divs = self.soup.find(class_="t_award_d").findAll("div")

        for div in badges_divs:
            parsed_str = badges_re.findall(str(div))[0]
            symbol = parsed_str[0]
            ru_name = parsed_str[1]
            date = parsed_str[2]
            result[badges_list[parsed_str[1]]] = {
                "symbol": symbol,
                "ru_name": ru_name,
                "date": date
            }
        return {"badges": result}

    def get_characteristics(self):
        characts_html = self.soup.find(id="characteristics").findAll("tr")
        # для некоторых выставим нули, вдруг их нет на странице
        characts = {"creatures_m": 0,
                    "creatures_f": 0,
                    "creatures_pairs": 0,
                    "creatures_comleted_at": "",
                    "savings": 0,
                    "shop": "",
                    "wood_cnt": 0,
                    "temple_completed_at": "",
                    "ark_completed_at": "",
                    "motto": ""}
        for charact in characts_html:
            label = str(charact.find(class_="label").text).strip()
            name = str(charact.find(class_="name").text).strip()
            # pass`ы добавил что бы в pycharm сворачивалось

            if label == "Возраст":
                characts["age"] = name
                pass
            if label == "Характер":
                characts["alignment"] = name
                pass
            if label == "Гильдия":
                if name == "не состоит":
                    characts["clan"] = name
                    characts["clan_position"] = ""
                else:
                    clan = re.findall("(.*)\((.*)\)", name.replace("\n", " "))[0]
                    characts["clan"] = clan[0].strip()
                    characts["clan_position"] = clan[1]
            if label == "Убито монстров":
                characts["monsters"] = name
                characts["monsters_num"] = self._str_to_num(name)
                pass
            if label == "Смертей":
                characts["deaths"] = int(name)
                pass
            if label == "Побед / Поражений":
                characts["wins"], characts["looses"] = \
                    re.findall("(\d+) / (\d+)", name)[0]
                characts["wins"], characts["looses"] = \
                    int(characts["wins"]), int(characts["looses"])
            if label == "Твари по паре":
                creat = re.findall("(\d+)м,\\xa0(\d+)ж \(([\d\.]+)%\)", name)[0]
                characts["creatures_m"] = creat[0]
                characts["creatures_f"] = creat[1]
                characts["creatures_pairs"] = int(float(creat[2])*10)
                characts["creatures_comleted_at"] = ""
            if label == "Твари собраны":
                characts["creatures_m"] = 1000
                characts["creatures_f"] = 1000
                characts["creatures_pairs"] = 1000
                characts["creatures_comleted_at"] = name
            if label == "Храм достроен":
                characts["temple_completed_at"] = name
                characts["bricks_cnt"] = 1000
            if label == "Кирпичей для храма":
                characts["bricks_cnt"] = int(name[:-1].replace(".", ""))
                pass
            if label == "Ковчег достроен":
                ark = re.findall("(.*)\((.*)\)", name.replace("\n", " "))[0]
                characts["ark_completed_at"] = ark[0].strip()
                characts["wood_cnt"] = int(ark[1][:-1].replace(".", ""))
                pass
            if label == "Дерева для ковчега":
                characts["wood_cnt"] = int(name[:-1].replace(".", ""))
                pass
            if label == "Сбережения":
                characts["savings"] = int(re.findall("(\d*)\D*", name)[0])
                pass
            if label == "Лавка":
                characts["shop"] = name[1:-1]
                pass
        return characts

    def get_equipment(self):
        items = self.soup.find(id="equipment").findAll("tr")
        equipment = []
        for item in items:
            equipment.append({"type": item.find(class_="label").text,
                              "name": item.find(class_="name").text,
                              "level": item.find(class_="value").text})
        return {"equipment": equipment}

    def get_skills(self):
        skills_list = self.soup.find(class_="b_list")
        skills = []
        if skills_list is not None:
            skills_list = skills_list.findAll("li")
            for skill_ in skills_list:
                skill = re.findall("""<li>(.*)<span> (\d+).*</span></li>""", str(skill_))[0]
                skills.append({"name": skill[0],
                               "level": skill[1]})
        return {"skills": skills}

    def get_panteons(self):
        panteons = []
        panteons_list = self.soup.find(id="panteons")
        for panteon in panteons_list.findAll("tr"):
            if panteon.find(class_="value") is None:
                pass
            elif panteon.find(class_="value").text == "−":
                pass
            else:
                panteons.append({
                    "name": panteon.find(class_="name").text,
                    "position": panteon.find(class_="value").text
                })
        return {"panteons": panteons}

    def get_achievements(self):
        achievements = []
        achievements_list = self.soup.find(id="ach_b")
        if achievements_list is not None:
            for ach in achievements_list.findAll("li"):
                ach_ = re.findall("(Заслуженный)?\s*(.*)\s*([1-3]-й степени)?", ach.text.strip())[0]
                ach_ = ach_[0] + " " + ach_[1] + " " + ach_[2]
                achievements.append(ach_.strip())
        return {"achievements": achievements}

    def get_chronicle(self):
        footer = self.soup.find(id="footer")
        if footer is None:
            return {"chronicle_update": ""}
        else:
            return {"chronicle_update": footer.text.strip()[-10:]}

    def get(self):
        page_data = {}
        try:
            page_data.update(self.get_levels())
        except TypeError:
            raise(Exception("God not found."))
        page_data.update(self.get_badges())
        page_data.update(self.get_characteristics())
        page_data.update(self.get_equipment())
        page_data.update(self.get_skills())
        page_data.update(self.get_panteons())
        page_data.update(self.get_achievements())
        page_data.update(self.get_chronicle())
        page_data.update(self.get_essential())

        """print("Уровни", self.get_levels())
        print("Значки", self.get_badges())
        print("Хар-ки", self.get_characteristics())
        print("Снаряжение", self.get_equipment())
        print("Умения", self.get_skills())
        print("Пантеоны", self.get_panteons())
        print("Заслуги", self.get_achievements())
        print("Хроника", self.get_chronicle())"""
        return page_data
