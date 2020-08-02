FROM python:3.6.8

WORKDIR /wrk

COPY . /wrk

RUN pip install -r requirements.txt && python build_database.py

EXPOSE 5000

CMD python server.py