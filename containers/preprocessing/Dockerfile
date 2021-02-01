FROM python:3.8-slim-buster

ADD ./requirements.txt .
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=TRUE

ADD resize_images.py /
ENTRYPOINT ["python3", "/processing_script.py"]