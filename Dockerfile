FROM ubuntu:16.04
MAINTAINER Hang Park <hangpark@kaist.ac.kr>

# Install packages
RUN apt-get update \
  && apt-get install -y \
    gcc \
    python3.5-dev \
    mysql-client \
    nginx \
    python-virtualenv \
    npm \
    nodejs-legacy \
    git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Configure Nginx
WORKDIR /etc/nginx/sites-available
ADD nginx.conf exampleproject
WORKDIR /etc/nginx/sites-enabled
RUN rm default \
  && ln -s ../sites-available/exampleproject ./exampleproject \
  && echo "\ndaemon off;" >> /etc/nginx/nginx.conf

# Configure uWSGI
RUN mkdir -p /tmp/uwsgi

# Download frontend dependencies
WORKDIR /app/exampleproject
ADD package.json package.json
ADD bower.json bower.json
RUN npm install \
  && node_modules/bower/bin/bower install --allow-root

# Set python virtual environment
WORKDIR /app/exampleproject
RUN mkdir -p /app/exampleproject
ADD requirements.txt requirements.txt
RUN virtualenv --python=python3 venv \
  && /bin/bash -c "source venv/bin/activate && pip install -r requirements.txt"

# Add whole project
WORKDIR /app/exampleproject
ADD ./ ./

# Configure Django settings
ENV DJANGO_SETTINGS_MODULE exampleproject.settings.production

# Compile frontends and collect static files
WORKDIR /app/exampleproject
RUN node_modules/gulp/bin/gulp.js \
  && /bin/bash -c "source venv/bin/activate && python manage.py collectstatic --noinput" 

# Compile document
WORKDIR /app/exampleproject/docs
RUN /bin/bash -c "source ../venv/bin/activate && make html"

# Move to root directory
WORKDIR /app/exampleproject

# Configure server encoding
ENV LANG C.UTF-8

# Expose ports
EXPOSE 80 443

# Run server
RUN chmod +x /app/exampleproject/docker-entrypoint.sh
ENTRYPOINT /app/exampleproject/docker-entrypoint.sh
