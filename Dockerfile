# Use a imagem base oficial do Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt e instale as dependências
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copie todo o código fonte para o contêiner
COPY ./app /app
COPY ./db /app/db

# Expõe a porta 8000 para que a aplicação possa ser acessada externamente
EXPOSE 8000

# Importante para importações estáticas
ENV PYTHONPATH="/"

# Comando para executar a aplicação quando o contêiner for iniciado
CMD ["uvicorn", "main:appServer", "--host", "0.0.0.0", "--port", "8000"]
