# --- Stage 1: Install Dependencies ---
FROM node:22-alpine AS deps
WORKDIR /app

# Check for package-lock.json and install exact dependencies
COPY package.json package-lock.json* ./
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# --- Stage 2: Build the Application ---
FROM node:22-alpine AS builder
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1

# Bring over installed node_modules from the deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Compile the Next.js production bundle
RUN npm run build

# --- Stage 3: Optimized Production Runner ---
FROM node:22-alpine AS runner
WORKDIR /app

# Ensure production flags and telemetry are locked down
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000 \
    HOST=0.0.0.0

# Copy only the compiled deployment build and essential static assets
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.ts ./next.config.ts

# Production port access mapping
EXPOSE 3000

# Execute the production start script
CMD ["npm", "run", "start"]