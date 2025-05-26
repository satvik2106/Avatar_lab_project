# Use official Node.js LTS image
FROM node:18

# Create app directory inside container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the backend code
COPY . .

# Expose port (replace 5000 with your backend port if different)
EXPOSE 5000

# Start the server
CMD ["node", "server.js"]
