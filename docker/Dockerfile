from python:alpine

RUN apk add --no-cache git postgresql-dev gcc libc-dev
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base

RUN pip install gunicorn
RUN pip install psycopg2
RUN pip install ipdb
RUN pip install ipython

WORKDIR /app

RUN git clone -b "ortosia-cabina" https://github.com/pablotabares/decide.git .
RUN pip install -r requirements.txt

WORKDIR /app/decide

ADD docker-settings.py /app/decide/local_settings.py

CMD ["sh", "-c", "python3 manage.py runserver 0.0.0.0:$PORT"]
