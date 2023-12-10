FROM python:3.9-slim

WORKDIR /backend

RUN pip install --upgrade pip

RUN pip install gunicorn==20.1.0

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

# RUN pip install netcat
# RUN chmod 777 starter.sh
# ENTRYPOINT ["bash", "/backend/starter.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi"]