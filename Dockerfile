FROM python:latest
COPY start.sh /start.sh
ENTRYPOINT ["/start.sh"]
