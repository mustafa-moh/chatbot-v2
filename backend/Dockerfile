FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install watchdog for efficient file change detection
RUN pip install watchdog

COPY . .

# Enable auto-reload with Flask's built-in reloader
CMD ["flask", "--app", "app/app.py", "run", "--host=0.0.0.0", "--port=5000", "--debug"]
