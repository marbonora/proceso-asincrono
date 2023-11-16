# Proceso asíncrono utilizando Celery
## Llamada POST para empezar el proceso
### `POST /async_process/start`
Un ejemplo de respuesta sería: 
```json
{
    "result_id": "0d51651c-2e0a-4104-ab37-c69814b43e50"
}
```
Nos guardamos el id para obtener el resultado del proceso, cuando esté disponible. 

## Llamada GET para obtener el resultado
### `GET /async_process/<result_id>` 
Si todavía no está disponible, devuelve:
```json
{
    "ready": false,
    "successful": false,
    "value": null
}
```
Si ya está disponible, el tendremos el resultado en el campo "value":
```json
{
    "ready": true,
    "successful": true,
    "value": "este es el resultado esperado"
}
```

## Requisitos
### [docker-compose](server/docker-compose.yml)
Servicio [Redis](https://redis.io/) en docker, que se encarga de la gestión y almacenamiento de los ids de tareas. 
```json
  redis: 
    image: redis:latest
    restart: always
    ports:
      - '6379:6379'
    volumes: 
    - ./data/redis:/root/redis
    - ./data/redis/redis.conf:/usr/local/etc/redis/redis.conf
```
### [Dockerfile](server/Dockerfile)
Importar Celery, Redis y exponer el puerto 6379
```
RUN pip install celery
RUN pip install redis==3.4.1
EXPOSE 6379
```

### [docker/run-redis.sh](server/docker/run-redis.sh)
Poner Redis en funcionamiento
```
#!/bin/bash
if [ ! -d redis-stable/src ]; then
    curl -O http://download.redis.io/redis-stable.tar.gz
    tar xvzf redis-stable.tar.gz
    rm redis-stable.tar.gz
fi
cd redis-stable
make
src/redis-server
```

### [docker/supervisor.conf](server/docker/supervisor.conf)
Llamar al worker de celery, que se inicia en [server.py](server/server.py)
´´´
[program:async_process]
command=/bin/sh -c "sleep 5 && cd /app/server && celery -A server.celery worker --loglevel=INFO -P gevent"
autorestart=true
startretries=10
´´´
### [server.py](server/server.py)
Inicializar Celery dentro del objeto Flask app. 
´´´
# Flask app starts
app = Flask(__name__)
# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'
# Init Celery
celery = Celery(app.name, broker = app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
´´´

Se configuran los endpoints para iniciar el proceso asíncrono y para obtener el resultado. 
´´´
@app.route('/async_process/start', methods=['POST'])
@app.route('/async_process/<process_id>', methods=['GET'])
´´´

### [async_process.py](server/async_process.py)
Se declara el método al que queremos llamar de forma asíncrona, con la etiqueta "shared_task"
´´´
@shared_task(ignore_result = False)
´´´
