FROM python:3.9.9
WORKDIR /app
COPY ./requirements2.txt .
RUN pip install -r ./requirements2.txt
COPY . /app/.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]