FROM python:3.10.0b2

WORKDIR /usr/src/app

COPY app.py .

# -u ensures print statements are printed to docker log
CMD [ "python", "-u", "./app.py" ]