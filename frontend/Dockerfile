# Dockerfile for frontend
FROM node:20-alpine

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy package files first for better caching
COPY package.json ./

# Copy source code
COPY . .

# Install dependencies
RUN pnpm install

# Expose port
EXPOSE 5173

# Start dev server with host binding for Docker
CMD ["pnpm", "dev", "--host", "0.0.0.0"]
