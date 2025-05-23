FROM python:3.11-slim


WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

ENV DEBUG=0
ENV DJANGO_SETTINGS_MODULE=hello_project.settings
ENV ALLOWED_HOSTS=*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN python manage.py collectstatic --noinput

RUN python manage.py migrate


EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "hello_project.wsgi:application"]
