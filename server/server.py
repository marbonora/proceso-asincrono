import sys, traceback, time, logging, json, os

import async_process
from flask import Flask, Response, request
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import pandas as pd
import numpy as np
from celery import Celery, Task
from celery.result import AsyncResult

print('- Configuring server logs...')
Path("/app/server/logs").mkdir(parents=True, exist_ok=True)
logger = logging.getLogger('server')
logger.setLevel(logging.DEBUG)
logger_handler = TimedRotatingFileHandler('/app/server/logs/server.log', when="d", interval=1)
logger.addHandler(logger_handler)
logger_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
logger_handler.setFormatter(logger_formatter)
logger_error = logging.getLogger('server_error')
logger_error.setLevel(logging.DEBUG)
logger_error_handler = TimedRotatingFileHandler('/app/server/logs/server_error.log', when="d", interval=1)
logger_error.addHandler(logger_error_handler)
logger_error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
logger_error_handler.setFormatter(logger_error_formatter)

print('Server started successfully')

# Flask app starts
app = Flask(__name__)
# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'
# Initi Celery
celery = Celery(app.name, broker = app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/', methods=['GET'])
def root() :
  return 'It works! Welcome :)'
 
# Llamada que pone en marcha el proceso que hacemos de forma asíncrona
@app.route('/async_process/start', methods=['POST'])
def start_async_process() :
  prueba = ""
  try :
    result = async_process.start_async_process.delay(prueba)

    return { "result_id": result.id }
  except Exception as e:
    logger.debug(f'{e}')
    logger_error.exception(f'{e}')
    return Response(status=500)

# Llamada que pide resultados del proceso, si ha terminado 
@app.route('/async_process/<process_id>', methods=['GET'])
def result_async_process(process_id) :
  result = AsyncResult(process_id)
  return {
    "ready": result.ready(),
    "successful": result.successful(),
    "value": result.result if result.ready() else None,
  }