# Base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the code
COPY . .

# Pass API URL as a build argument
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Build the app
RUN npm run build

# Serve using a simple HTTP server
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]

# Expose the app on port 3000
EXPOSE 3000
