FROM python:3.13.2-slim

WORKDIR /test

COPY . .

RUN pip install -r requirements.txt && python -m playwright install --with-deps

VOLUME ["/test/report_docker"]

CMD ["sleep", "infinity"]