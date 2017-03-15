# godville-unofficial-api

Неофициальное API для godville.net

Состоит из:
* Парсер для страницы бога.
* Скрипта для произведения запроса.
* Пример файла для добавления в cron для ежедневного сбора статистики.
* Пример веб-сервера для обработки запросов к странице бога и API.

Для запуска требуется Python 3 и внешние библиотеки из файла requirements.txt

Пример можно увидеть тут http://gvapi.g0fs.com/

Значения, возвращаемые этим API:

1. Значения, которые берутся со страницы бога

|Ключ|Тип|Содержание|
|--- | --- | ---
|hero_name|string|Имя героя
|hero_gender|string|Пол героя (f или m)
|god_name|string|Имя бога
|god_gender|string|Пол бога (f или m)
|avatar_url|string|URL аватара
|hero_lvl|int|Уровень героя
|trader_lvl|int|Уровень торговца (0 пока нет лавки)
|motto|string|Девиз (Пустая строка, если нет)
|badges|object|Объект, содержащий медали (храм, звероводство и тому подобное)
|age|string|Возраст героя
|alignment|string|Характер
|clan|string|Гильдия
|clan_position|string|Статус в гильдии (если не состоит в гильдии, то пустая строка)
|monsters|string|Количество убитых монстров стрококй (около N тысяч)
|monsters_num|string|Количество убитых монстров числом (приблизительное)
|deaths|int|Количество смертей
|wins|int|Количество побед
|looses|int|Количество поражений
|ark_completed_at|string|Дата окончания ковчега
|wood_cnt|int|Количество брёвен (0, если не окончен храм)
|temple_completed_at|string|Дата окончания храма
|bricks_cnt|int|Количество кирпичей (1000, если храм построен)
|savings|int|Сбережения (количество тысяч)
|creatures_completed_at|string|Дата сбора существ
|creatures_pairs|float|Количество полных пар
|creatures_m|int|Количество самцов
|creatures_f|int|Количество самок
|shop|string|Название лавки (пустая строка, если нет)
|equipment|object|Снаряжение героя
|skills|object|Умения
|panteons|object|Пантеоны
|achievements|object|Заслуги
|chronicle_update|string|Дата последнего обновления хроники

2. Значения, доступные только в открытой части малого API

Ключ|Тип|Содержание|
--- | --- | ---
inventory_max_num|int|Максимальный размер инвентаря
max_health|int|Максимальный запас здоровья
savings_completed_at|string|Дата сбора пенсии

3. Прочее

|Ключ|Тип|Содержание|
|--- | --- | ---
|update_time|int|unix timestamp времени, когда были получны эти данные

4. Пояснения к объектам

* badges: содержит 4 объекта: temple, ark, pet и creatures. Если медаль ещё не получена, то {"temple": None}
 А если получена, то содержит {"temple":{"symbol": "庙", "ru_name": "Храмовладелец", "date": "11.11.2013 20:57"}}
* equipment: массив из 7 элементов, каждый из которых содержит {"type": "Оружие", "name": "орудие труда", "level": "+116"}
 или {"type": "Ноги", "name": "пусто", "level": ""}
* skills: массив умений ("name": "маскировка под дуб", "level": "98")
* panteons: массив пантеонов: {"name": "Мощи", "position": "771"}
* achievements: массив строк ["Заслуженный Заводчик", ...]
* inventory: массив, содержащий вещи из инвентаря, в том порядке, в каком они у героя.

|Ключ|Тип|Содержание|
|--- | --- | ---
|name|string|Название трофея
|cnt|int|Количество этого трофея в инвентаре
|bold|bool|Жирный
|heal_potion|bool|Лечилка
|activate_by_user|bool|Активируемый
|needs_godpower|int|Количество праны для активации (0 у неактивируемых)
|description|string|Описание трофея (для активируемых)