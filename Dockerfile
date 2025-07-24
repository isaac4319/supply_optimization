# Use a slim Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy only the requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the repo
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Use an environment file for secrets
# When you run, pass --env-file .env

# Run Streamlit in headless mode
ENTRYPOINT ["streamlit", "run", "Dashboard/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
