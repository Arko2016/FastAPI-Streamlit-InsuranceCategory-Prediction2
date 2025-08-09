#Install base image
FROM python:3.11-slim

#Set working directory
WORKDIR /app

#Copy requirements to working directory
COPY requirements.txt .

#Install packages mentioned under requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#Copy rest of application code
COPY . .

#Expose application port
EXPOSE 8000

#Specify command for running the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
