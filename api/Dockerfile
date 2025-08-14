FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expone el puertoadded:0
EXPOSE 8000

# Run FastAPI app (recuerda cambiar si usas otra carpeta o archivo)
CMD ["bash", "start.sh"]
