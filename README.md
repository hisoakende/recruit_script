## Запуск для разработки

1. Установить необходимые зависимости

```bash
pip install -r ./requirements.txt
```

2. Запустить сервис

```bash
gunicorn src.main:app --worker-class uvicorn.workers.UvicornWorker

```

## Production

1. Настроить окружение
2. Собрать образ

```bash
docker build . -t recruit_script
```

3. Запустить контейнер

```bash
docker run -p "8000:8000" recruit_script
```
