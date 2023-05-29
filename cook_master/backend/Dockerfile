# Development

# pull official base image
FROM tiangolo/uwsgi-nginx-flask:python3.8

# set work directory
WORKDIR /usr/backend
# copy project
COPY . .

# set python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=${PYTHONPATH}:/usr/backend

# install dependencies
RUN pip install --upgrade pip
RUN pip install pip-tools


RUN pip install -r requirements.txt

# install system dependencies
RUN apt-get update && apt-get install -y netcat
# run entrypoint
ENTRYPOINT ["python", "app.py"]
