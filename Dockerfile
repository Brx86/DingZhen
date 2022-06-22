FROM python:latest
RUN git clone https://github.com/Brx86/DingZhen -b api --depth=1 \
    && cd DingZhen \
    && pip install -r requirements.txt
ENTRYPOINT ["python3 app.py"]