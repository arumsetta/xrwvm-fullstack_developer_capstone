# Use Python base image
FROM python:3.12.0-slim-bookworm

# Set environment variables
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1
ENV APP=/app

# Set working directory
WORKDIR $APP

# Copy requirements and install them
COPY requirements.txt $APP/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy the rest of the files
COPY . $APP

# Expose the port your app will run on
EXPOSE 8000

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]

# Default command to start the application
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
