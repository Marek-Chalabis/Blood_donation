# pillow wont work on alpine version
FROM python:3.8

# # install selenium/chromedriver
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE `/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV SECRET_KEY=&)k3&=_%c7@5035@l0+)d2j^nl_+@w)z(@nik0ce%qs3ue2n5v
ENV ALLOWED_HOSTS=*

ENV EMAIL_HOST_USER=***
ENV EMAIL_HOST_PASSWORD=***

ENV AWS_ACCESS_KEY_ID=***
ENV AWS_SECRET_ACCESS_KEY=***
ENV AWS_STORAGE_BUCKET_NAME=***

RUN mkdir /app
WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py createcachetable

# simulates CI test/builds
RUN pytest

# populate DB
RUN python Assets/fill_db_blood_donation.py
RUN python manage.py populate_db /app/dummy_data -a

CMD python manage.py runserver 0.0.0.0:$PORT