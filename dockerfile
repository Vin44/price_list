FROM python:3.11-slim-bullseye

WORKDIR /app

# Install system deps + MS repo keys
RUN apt-get update && apt-get install -y \
    curl gnupg2 apt-transport-https ca-certificates gcc g++ unixodbc-dev \
    libnss3 libxcomposite1 libxrandr2 libxdamage1 libatk1.0-0 \
    libasound2 libxkbcommon0 libgtk-3-0 \
 && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg \
 && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
 && apt-get update \
 && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install-deps && playwright install

# Create data folder
RUN mkdir -p /app/data

# Copy app code
COPY . .

CMD ["python", "main.py"]