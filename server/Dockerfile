FROM python:3.9-alpine

WORKDIR /app

RUN apk update && apk add --no-cache build-base postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD ["uvicorn", "holowhoslive.main:app", "--host", "0.0.0.0", "--port", "80"]
CMD uvicorn holowhoslive.main:app --host 0.0.0.0 --port $PORT
