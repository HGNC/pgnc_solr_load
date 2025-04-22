FROM python:latest

WORKDIR /usr/src/app

# Install system dependencies first
RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    build-essential \
    gcc g++ \
    libffi-dev \
    libssl-dev \
    wget \
    lsb-release

# Install PostgreSQL 17 client (fixed version)
RUN echo "deb [arch=amd64,arm64] http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/postgresql.gpg && \
    apt-get update && \
    apt-get install -y postgresql-client-17

# Python dependencies
COPY requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip setuptools wheel cython && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apt-get clean

# Prepare environment
RUN mkdir -p /usr/src/app/output && \
    mkdir -p /usr/src/app/input && \
    mkdir -p /usr/src/app/db-data

CMD ["sh", "-c", "/usr/src/app/bin/update.sh"]
