FROM python

RUN apt-get  update -y && apt-get upgrade -y
# RUN apt-get install build-essential -y
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV FLASK_APP=router
ENV FLASH_ENV=development
ENV APP_SETTINGS=settings.cfg

COPY . /src
WORKDIR /src
ENTRYPOINT [ "uwsgi" ]
CMD [ "--ini", "uwsgi.ini" ]