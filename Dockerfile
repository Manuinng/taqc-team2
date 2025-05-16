FROM jenkins/jenkins:lts
LABEL maintainer="TAQC Team 2"
LABEL description="Jenkins with Python and Playwright"
EXPOSE 8080
USER root

WORKDIR /var/jenkins_home/workspace

COPY . .

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv

RUN python3 -m venv venv

VOLUME ["/test/report_docker"]

CMD ["/usr/bin/tini", "--", "/usr/local/bin/jenkins.sh"]