FROM python:3.9

WORKDIR /app

COPY . /app

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

CMD ["./wait-for-it.sh", "db:3306", "--", "python", "./demobotrista/manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["tail", "-f", "/dev/null"]