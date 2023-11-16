from celery import shared_task
import time, json


print('Async process...')

@shared_task(ignore_result = False)
def start_async_process(documents):
    try:
        result = "este es el resultado esperado"
        time.sleep(30)
        return result
    except Exception as e:
        print(e)
        return e