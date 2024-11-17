FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
RUN poetry --version

WORKDIR /app
COPY . .
RUN poetry install
EXPOSE 8081
CMD ["poetry", "run", "python", "src/service.py"]
