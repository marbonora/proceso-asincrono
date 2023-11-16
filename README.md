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
### [a relative link](server/docker-compose.yml)
