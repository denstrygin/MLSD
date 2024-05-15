FROM node:alpine
WORKDIR /app
COPY . .
RUN yarn install
COPY . .
EXPOSE 3000
CMD ["yarn", "start"]