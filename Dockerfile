# pull official base image
FROM docker.arvancloud.ir/python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y netcat

# copy entrypoint.sh
COPY ./entrypoint.sh .
# COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .


# run entrypoint.sh
# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
# CMD ["run"]

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] # in case we don't have docker_compose file
#CMD sleep 10 && \
