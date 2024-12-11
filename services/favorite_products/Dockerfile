
FROM python:3.12.7-slim

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /api
COPY /services/favorite_products/ .

RUN python -m pip install -r requirements.txt

RUN apt-get -y update && apt-get -y install curl

RUN adduser -u 5678 --disabled-password --gecos "" apiuser && chown -R apiuser /api
USER apiuser

CMD ["./run.sh"]
