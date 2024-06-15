# docker build -t mcortes027/alina_rag:latest .
# Use the official Python 3.11 image as the base image
FROM python:3.11 

RUN apt-get update
RUN apt-get install -y iputils-ping 
RUN apt-get install -y net-tools
# Set the working directory inside the container
WORKDIR /app

# Copy everything from the local 'app' directory to the '/app' directory in the container
COPY . .

# Optionally, if you have a requirements.txt file, you can uncomment the next line to install Python dependencies
RUN pip install -r requirements.txt

# Command to run when the container starts (example: running a Python script)
# CMD ["python", "your_script.py"]