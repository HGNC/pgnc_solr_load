FROM python:latest

WORKDIR /usr/src/app

# Copy requirements first for better caching
COPY requirements.txt ./requirements.txt

RUN apt-get update && apt-get install -y python3-pip build-essential gcc g++ libffi-dev libssl-dev

# Upgrade pip and install requirements
RUN pip3 install --upgrade pip setuptools wheel cython && \
    pip3 install --no-cache-dir -r requirements.txt

RUN apt-get clean

# Copy the rest of the application
COPY bin/data-update ./data-update
COPY bin/update.sh ./update.sh

# Make script executable
RUN chmod +x ./data-update/main.py
RUN mkdir -p /usr/src/app/output

    # Run the script
CMD ["/usr/bin/bash", "/usr/src/app/update.sh"]
