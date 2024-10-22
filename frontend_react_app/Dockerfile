# Use uma imagem do Node.js como base
FROM node:18-alpine

# Definir o diretório de trabalho
WORKDIR /usr/src/app

# Copiar os arquivos package.json e package-lock.json (se existirem)
COPY package*.json ./

# Instalar as dependências (incluindo o expo-cli localmente)
RUN npm install

# Instalar o Expo CLI de forma local (não global)
RUN npx expo install

# Copiar o restante dos arquivos do projeto (se aplicável)
COPY . .

# Expor a porta que o Expo vai utilizar (opcional)
EXPOSE 19000

# Comando padrão para manter o container em execução
CMD ["sh", "-c", "while :; do sleep 10; done"]
