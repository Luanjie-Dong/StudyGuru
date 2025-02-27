FROM python:3-slim
WORKDIR /database
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./supabaseClient.py .
COPY module.py .
CMD ["python", "module.py"]