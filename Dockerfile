FROM python:3.12.6-bookworm

WORKDIR /my_app

ENV PYTHONPATH=/my_app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip wheel

RUN pip install "poetry==2.2.1"

RUN poetry config virtualenvs.create true

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY src ./src

CMD ["poetry", "run", "python", "src/main.py"]