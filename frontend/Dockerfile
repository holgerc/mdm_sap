FROM node:20-alpine

WORKDIR /app

# Configure npm to handle SSL issues (corporate proxy)
RUN npm config set strict-ssl false

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start development server
CMD ["npm", "run", "dev"]
