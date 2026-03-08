FROM node:22-alpine

WORKDIR /app

# 1. Sadece package dosyalarını kopyala
COPY package*.json ./

# 2. Paketleri kur (package.json değişmedikçe burası 0 saniye sürer)
RUN npm install

#RUN npm install --prefer-online

# 3. Kodu kopyala
COPY . .

CMD ["npm", "run", "start:dev"]