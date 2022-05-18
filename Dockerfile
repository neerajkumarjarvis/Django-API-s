FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /panna
WORKDIR /panna
RUN pip install --upgrade pip
COPY requirements.txt /panna/

RUN pip install -r requirements.txt
COPY . /panna/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
