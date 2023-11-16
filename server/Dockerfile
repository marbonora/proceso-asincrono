FROM python:3.10
WORKDIR /app
RUN apt-get update && apt-get install -y supervisor nginx nano less curl g++ protobuf-compiler libprotobuf-dev \
 && adduser --disabled-password --gecos 'www' www
RUN pip install --no-cache-dir --upgrade pip
RUN pip install pip-licenses
RUN pip install gunicorn
RUN pip install flask
RUN pip install regex
RUN pip install scikit-learn==1.0.2
RUN pip install superlance
RUN pip install pyyaml
RUN pip install requests
RUN pip install pandas
RUN pip install numpy
RUN pip install openpyxl
RUN pip install datetime
RUN pip install gevent==22.10.2
RUN pip install celery
RUN pip install redis==3.4.1
RUN pip install nltk

COPY docker /app/docker
COPY . /app/server
ARG mode=prod
RUN chmod +x /app/docker/entrypoint.sh \
   && if [ "$mode" = "prod" ]; then echo 'Building for production...' \
   && cd /app/server \
   && python -m compileall -f -b async_process.py server.py \
   && rm -rf .dockerignore .gitignore Dockerfile docker docker-compose.yml __pycache__ *.py \
   && cd ..; fi
ENV SERVER_WORKERS=2
ENV SERVER_THREADS=2
ENV PROCESS_WORKERS=10
ENV PROCESS_SELECT=100
ENV TIMEOUT=200
ENV EMAIL_ACCOUNT=admin@example.com
EXPOSE 9000
EXPOSE 5601
EXPOSE 6379

ENTRYPOINT [ "/app/docker/entrypoint.sh" ]
