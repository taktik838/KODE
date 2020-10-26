# KODE

Этот проект создан для тестового задания от KODE

[Диаграмма компонентов системы](high_level_design_diagram.png)

В [db.py](db.py) находятся функции для работы с базой данных. Не подрозумевает публичный API.

В [delivery_area.py](delivery_area.py) находится основная часть задания. Тут находятся публичное API. 

[database.db](database.db) это локальная база данных, с ней работает модуль db.

[openapi.yaml](openapi.yaml) тут хранится openapi.

[simulate.ipynb](simulate.ipynb) тут тесты.