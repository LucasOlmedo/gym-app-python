# Use uma imagem Node apropriada
FROM node:20

# Defina o diretório de trabalho no contêiner
WORKDIR /usr/src/app

# Copie o package.json e o package-lock.json para o contêiner
COPY ./app/package*.json ./

# Instale as dependências do projeto, incluindo expo-cli
RUN npm install

# Instale o Expo CLI localmente como dependência de desenvolvimento
RUN npm install --save-dev expo-cli
RUN npm install --global eas-cli

# Copie todo o conteúdo do projeto para o contêiner
COPY ./app .

# Exponha as portas usadas pelo Expo
EXPOSE 19000 19001 19002

# Comando para iniciar o Expo com o npx
CMD ["npx", "expo", "start"]
