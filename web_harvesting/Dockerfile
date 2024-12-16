FROM python:3.12-slim


# Environment variables for Airflow
ENV AIRFLOW_HOME=/opt/airflow
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies, including wget and Chrome dependencies
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    curl \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    xvfb \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libgbm1 \
    libgtk-3-0 \
    libpango-1.0-0 \
    libvulkan1 \
    libxcomposite1 \
    libxdamage1 \
    libxkbcommon0 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install ./google-chrome-stable_current_amd64.deb -y \
    && rm ./google-chrome-stable_current_amd64.deb

# Copy only the necessary files for dependency installation
WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Install Poetry and project dependencies
RUN pip install poetry==1.8.5 \
    && poetry install --no-interaction --no-ansi

# Install Apache Airflow
RUN pip install apache-airflow[postgres,docker]==2.7.1

# Copy the rest of the application files
COPY . /app

# Set default command for the container
CMD ["airflow", "standalone"]
