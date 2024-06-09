FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=/src

WORKDIR /src


COPY requirements.txt /tmp/

RUN apk add --virtual .build-deps --no-cache postgresql-libs postgresql-dev gcc python3-dev musl-dev && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    apk --purge del .build-deps

COPY . /src/

CMD ["python", "run.py"]