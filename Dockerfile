FROM python:latest

WORKDIR /usr/src/app

# Copy requirements first for better caching
COPY requirements.txt ./requirements.txt

# Upgrade pip and install requirements
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY bin/data-update ./data-update
COPY bin/update.sh ./update.sh

# Make script executable
RUN chmod +x ./data-update/main.py 

    # Run the script
CMD ["/usr/bin/bash", "/usr/src/app/update.sh"]