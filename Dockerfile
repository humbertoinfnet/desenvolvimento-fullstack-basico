# Use a imagem base do Python 3.11.3
FROM python:3.11.3

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo do diretório atual para o diretório de trabalho no contêiner
COPY . .

# Comando a ser executado ao iniciar o contêiner
CMD [ "python", "./app.py" ]