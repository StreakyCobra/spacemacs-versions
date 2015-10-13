FROM ubuntu:15.10
MAINTAINER Fabien Dubosson <fabien.dubosson@gmail.com>

# Set locale
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

# Update the system
RUN apt-get update && apt-get upgrade -y

# Install emacs
RUN apt-get install -y emacs git && \
    rm -rf /var/lib/apt/lists/* 

# Create `emacs` user
RUN useradd -ms /bin/bash emacs

# Switch to `emacs` user
ENV HOME /home/emacs
USER emacs

# Needed by `exec-path-from-shell`
ENV SHELL /bin/bash

WORKDIR /home/emacs

ENTRYPOINT ["emacs"]
