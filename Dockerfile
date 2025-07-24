FROM python:3.9

# Set working directory
WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y unzip wget

# Install ngrok
RUN wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip && \
    unzip ngrok-v3-stable-linux-amd64.zip && \
    mv ngrok /usr/local/bin && \
    rm ngrok-v3-stable-linux-amd64.zip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Runtime entrypoint
CMD ["bash", "-c", "ngrok config add-authtoken $NGROK_AUTHTOKEN && streamlit run Dashboard/streamlit_app.py --server.port=8501 --server.address=0.0.0.0"]
