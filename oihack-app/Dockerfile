FROM node:23-alpine

WORKDIR /app

COPY package*.json ./

# RUN npm install -g npm@11.4.0
RUN npm install

COPY . .

RUN npm run build

CMD ["npm", "run", "start"]