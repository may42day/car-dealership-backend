FROM python:3.10.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install -U pipenv
RUN pipenv install --system

COPY . /app
RUN python manage.py collectstatic --noinput

RUN mkdir -p /app/logs
RUN chmod -R 755 /app/logs

EXPOSE 8000
# ENTRYPOINT ["python"] 
# CMD ["manage.py", "runserver", "0.0.0.0:8000"]