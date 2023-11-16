# Celery
## Llamada POST para empezar el proceso
### `POST /async_process/start`
```json
{
    "result_id": "0d51651c-2e0a-4104-ab37-c69814b43e50"
}
```

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