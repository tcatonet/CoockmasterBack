# Development

# pull official base image
FROM tiangolo/uwsgi-nginx-flask:python3.8

# set work directory
WORKDIR /usr/tests
# copy project
COPY . .

# set python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=${PYTHONPATH}:/usr/tests

# install dependencies
RUN pip install --upgrade pip
RUN pip install pip-tools
RUN pip install -r requirements.txt

# install system dependencies
# run entrypoint
ENTRYPOINT ["python", "main_integration.py"]

