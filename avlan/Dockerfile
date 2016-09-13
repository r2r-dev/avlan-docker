FROM ubuntu:16.04
MAINTAINER Artur Stachecki <artur.stachecki@gmail.com>

ENV DEBIAN_FRONTEND noninteractive
ENV APPDIR /app
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Set locale to UTF-8
RUN locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
RUN locale-gen fr_FR.UTF-8

# Update python
RUN apt-get -qq update && \
    apt-get -y upgrade && \
    apt-get install -y \
        python libxml2-dev libxslt1-dev expat libevent-dev wget python-dev \
        texlive texlive-latex-extra language-pack-en unzip git python-pip \
        zlib1g-dev lib32z1-dev libpq-dev gettext curl latex2html && \
        libmysqlclient-dev \
    apt-get clean

# Install test dependencies
RUN pip install -q \
    virtualenv \
    pep8 \
    mock \
    nose \
    coverage \
    pylint

# Setting up virtualenv
RUN virtualenv /venv

# Add user py
RUN adduser --gecos 'py' --disabled-password py

RUN rm -fr $APPDIR && mkdir -p $APPDIR && cd /tmp

ADD config /

RUN /bin/avlan-install.sh

# Docker config
EXPOSE 8000
VOLUME ["/app"]
CMD ["/bin/avlan-start.sh"]
