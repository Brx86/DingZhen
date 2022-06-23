FROM python:latest
COPY start.sh /start.sh
ENTRYPOINT ["bash", "/start.sh"]
