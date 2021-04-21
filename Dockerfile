FROM python:3.8-alpine

# Install libraries
COPY requirements.txt /
COPY docker/entrypoint.sh /entrypoint.sh
RUN apk add --no-cache libmagic build-base \
    && pip install -r /requirements.txt \
    && chmod +x /entrypoint.sh 

# Install the app
COPY run.py /usr/local/bin/ecs-render
COPY ecs_render/ /usr/local/lib/python3.8/site-packages/ecs_render

# Install further integration
WORKDIR /src
ENTRYPOINT [ "/entrypoint.sh" ]