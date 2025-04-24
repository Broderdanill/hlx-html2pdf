FROM python:3.12-slim

# Install packages needed by Microsoft Edge and PDF-generation
RUN apt-get update && apt-get install -y \
    curl gnupg software-properties-common \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 libxss1 libxtst6 lsb-release wget \
    xdg-utils libdrm2 libxcomposite1 libxrandr2 libgbm1 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install Microsoft Edge (stable version)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg && \
    install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/ && \
    sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list' && \
    apt-get update && apt-get install -y microsoft-edge-stable && \
    rm microsoft.gpg

# Copy requirements.txt to the container
COPY requirements.txt /app/

# Install Python-dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application
WORKDIR /app
COPY app.py .

# Run with Gunicorn
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
