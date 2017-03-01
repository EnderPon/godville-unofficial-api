# godville-unofficial-api

Неофициальное API для godville.net

Состоит из:
* Парсер для страницы бога.
* Парсер для модификации "малого" API.
* Скрипта для произведения запроса.
* Пример файла для добавления в cron для ежедневного сбора статистики.
* Пример веб-сервера для обработки запросов к странице бога и малому API.

Для запуска требуется Python 3 и внешние библиотеки из файла requirements.txt

Пример можно увидеть тут http://gvapi.g0fs.com/

Значения, возвращаемые этим API:

1. Значения, которые берутся со страницы бога

|Ключ|Тип|Содержание|
|--- | --- | ---
|hero_name|string
|hero_gender|string
|god_name|string
|god_gender|string
|avatar_url|string
|hero_lvl|int
|trader_lvl|int
|motto|string
|badges|object
|age|string
|alignment|string
|clan|string
|clan_position|string
|gold|string
|gold_num|int
|monsters|string
|monsters_num|string
|deaths|int
|wins|int
|looses|int
|ark_completed_at|string
|wood_cnt|int
|temple_completed_at|string
|bricks_cnt|int
|savings|int
|creatures_completed_at|string
|creatures_percent|float
|exp_progress|int
|creatures_m|int
|creatures_f|int
|shop|string
|equipment|object
|skills|object
|panteons|object
|achievements|object
|chronicle_update|string

2. Значения, доступные в открытой части малого API

Ключ|Тип|Содержание|
--- | --- | ---
inventory_max_num|int
max_health|int
savings_completed_at|string

3. Значения из оперативного API

|Ключ|Тип|Содержание|
|--- | --- | ---
|health|int
|arena_fight|bool
|godpower|int
|inventory|object
|diary_last|string
|update_time|int
|expired|bool
|aura|string
|trader_lvl|int
|quest_progress|int
|distance|int
|quest|string
|town_name|string
|fight_type|string
|inventory_num|int
