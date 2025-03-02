FROM python:3-slim
WORKDIR /database
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY invokes.py .
COPY handle_upload.py .
CMD ["python", "handle_upload.py"]