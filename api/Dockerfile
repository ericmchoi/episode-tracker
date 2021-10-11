FROM python:3.10-alpine3.14
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENV FLASK_APP=ep_tracker_api

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "ep_tracker_api:create_app()"]
