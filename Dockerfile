FROM node:20-bookworm-slim AS builder
WORKDIR /usr/src/app

ARG PORT=3000

COPY package.json package-lock.json* ./
RUN npm ci

COPY src ./src
COPY ai_models ./ai_models
COPY tsconfig.json ./

RUN npm run build

FROM node:20-bookworm-slim AS runner
WORKDIR /usr/src/app

ARG PORT=3000

# Add Python for the prediction model
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gfortran \
        liblapack-dev \
        libopenblas-dev \
        python3 \
        python3-dev \
        python3-pip \
        python3-venv \
    && rm -rf /var/lib/apt/lists/*

ENV PORT=${PORT}
ENV NODE_ENV=production

COPY package.json package-lock.json* ./
RUN npm ci --omit=dev

COPY --from=builder /usr/src/app/dist ./dist
COPY --from=builder /usr/src/app/ai_models ./ai_models

RUN python3 -m venv /opt/venv \
	&& /opt/venv/bin/pip install --no-cache-dir -r ai_models/heart_model/requirements.txt

ENV PYTHON_BIN=/opt/venv/bin/python

EXPOSE ${PORT}
CMD ["node", "dist/http-server.js"]