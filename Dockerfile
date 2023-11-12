FROM python:3.11-slim

WORKDIR /app

COPY . /app/
RUN apt-get update && apt-get install -y curl && apt-get clean
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements-docker.txt

CMD python manage.py migrate \
#    && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser('root@example.com', 'root')" \
    && python manage.py collectstatic --no-input \
    && gunicorn DRFEdu.wsgi:application --bind 0.0.0.0:8000 --log-level info