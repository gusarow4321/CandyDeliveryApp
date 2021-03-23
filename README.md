Вступительное испытание в Школу бэкенд-разработки Яндекса
==============

Приложение нужно упаковать в Docker-контейнер и развернуть с помощью Ansible.

Внутри Docker-контейнера доступны две команды:
* `candy-db` — утилита для управления состоянием базы данных и
* `candy-api` — утилита для запуска REST API сервиса.

Как использовать?
=================
Как применить миграции:

```shell
docker run -it \
-e CANDY_DB_URL=postgresql://user:12345@localhost/candy \
gusarow4321/backendschool2021 candy-db upgrade head
```
Как запустить REST API сервис локально на порту 8080:

```shell
docker run -it -p 8080:8081 \
-e CANDY_DB_URL=postgresql://user:12345@localhost/candy \
gusarow4321/backendschool2021
```
Все доступные опции запуска любой команды можно получить с помощью
аргумента `--help`:

```shell
docker run gusarow4321/backendschool2021 candy-db --help
docker run gusarow4321/backendschool2021 candy-api --help
```
Опции для запуска можно указывать как аргументами командной строки, так и
переменными окружения с префиксом `CANDY` (например: вместо аргумента
`--db-url` можно воспользоваться `CANDY_DB_URL`).

Как развернуть?
---------------
Чтобы развернуть и запустить сервис на серверах, добавьте список серверов в файл
deploy/hosts.ini (с установленной Ubuntu) и выполните команды:

```shell
python setup.py sdist
docker build -t gusarow4321/backendschool2021:0.0.1 .
cd deploy
docker save -o image.tar gusarow4321/backendschool2021:0.0.1
ansible-playbook -i hosts.ini --user=root deploy.yml
```

Как запустить тесты локально?
-----------------------------
```shell
pytest
```