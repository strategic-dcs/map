FROM node:20-alpine
WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

EXPOSE 3000

COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent

COPY . ./

CMD ["npm", "run", "dev"]
