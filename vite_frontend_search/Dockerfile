# 1. Node.js 18 yerine 20 (veya 22) kullanıyoruz
FROM node:22-alpine

WORKDIR /app

# Context ../ olduğu için yolları doğru belirtelim
COPY vite_frontend_search/package*.json ./

RUN npm install

COPY vite_frontend_search/ .

# Vite'i çalıştır
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]