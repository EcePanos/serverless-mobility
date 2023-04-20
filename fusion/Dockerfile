FROM python:3.10-alpine
COPY . /app
WORKDIR /app

# Install the requirements for psycopg2
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
# Install the requirements for the app
RUN pip install -r requirements.txt
CMD ["python3", "fusion.py"]