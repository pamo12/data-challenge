FROM python:3.10

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY pipeline.py ./

ENTRYPOINT ["python3", "-m", "pipeline"]
