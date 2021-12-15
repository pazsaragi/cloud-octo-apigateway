# FROM tiangolo/uvicorn-gunicorn:python3.8-slim

# COPY ./requirements.txt /app/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# COPY ./app /code/app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# 
FROM python:3.8 as build

# 
WORKDIR /tmp

# 
RUN pip install poetry

# 
COPY ./pyproject.toml ./poetry.lock* /tmp/

# 
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# 
FROM tiangolo/uvicorn-gunicorn:python3.8-slim

# 
COPY --from=build /tmp/requirements.txt /app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 
COPY ./app /app/app

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
