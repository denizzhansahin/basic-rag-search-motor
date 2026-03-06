FROM node:18-alpine

WORKDIR /app

# 1. Sadece package dosyalarını kopyala
COPY package*.json ./

# 2. Paketleri kur (package.json değişmedikçe burası 0 saniye sürer)
RUN npm install

# 3. Kodu kopyala
COPY . .

CMD ["npm", "run", "start:dev"]