# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /order_management

# Copy project files
COPY . /order_management

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "run.py"]
