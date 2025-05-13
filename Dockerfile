FROM jenkins/jenkins:lts
USER root
ENV JENKINS_HOME=/home/jenkins_home

WORKDIR /home

COPY . .

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv 

RUN pip install -r requirements.txt -m playwright install --with-deps

VOLUME ["/test/report_docker"]

CMD ["sleep", "infinity"]