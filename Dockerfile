FROM python:3.9

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install ngrok manually
RUN apt-get update && apt-get install -y unzip wget && \
    wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip && \
    unzip ngrok-v3-stable-linux-amd64.zip && mv ngrok /usr/local/bin && rm ngrok-v3-stable-linux-amd64.zip

# Copy app
COPY . .

# Expose port
EXPOSE 8501

# Default command to run app and ngrok
CMD streamlit run Dashboard/streamlit_app.py --server.port=8501 --server.address=0.0.0.0 &