FROM python:3.10-alpine

# RUN apt-get  update -y && apt-get upgrade -y
# RUN apt-get install gcc libc-dev linux-headers -y
RUN apk add --no-cache gcc libc-dev linux-headers
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV FLASK_APP=router
ENV FLASH_ENV=development
ENV APP_SETTINGS=settings.cfg

COPY . /src
WORKDIR /src
ENTRYPOINT [ "uwsgi" ]
CMD [ "--ini", "uwsgi.ini" ]