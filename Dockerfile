FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt ./
RUN apt update
RUN apt-get install gdal-bin -y
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# CMD ["bash"]

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
