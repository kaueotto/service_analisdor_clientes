# Usar uma imagem base oficial do Python
FROM python:3.11-slim

# Configurar variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.4.2

# Criar e definir o diretório de trabalho no container
WORKDIR /app

# Instalar dependências do sistema para o Poetry e Kafka
RUN apt-get update && apt-get install -y \
    curl \
    netcat && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    apt-get clean

# Copiar os arquivos do projeto para o container
COPY . .

# Instalar as dependências do projeto com Poetry
RUN poetry install --no-dev

# Expor a porta usada pela aplicação Flask (ajuste conforme necessário)
EXPOSE 8081

# Configurar o comando de inicialização
CMD ["poetry", "run", "python", "src/service.py"]
