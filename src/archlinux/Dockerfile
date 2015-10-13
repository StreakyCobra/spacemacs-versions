FROM l3iggs/archlinux:latest
MAINTAINER Fabien Dubosson <fabien.dubosson@gmail.com>

# Set locale
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

# Update the system
RUN pacman -Syyu --noconfirm

# Install emacs
RUN pacman -S --noconfirm \
      xorg-server \
      emacs \
      git \
    && rm -rf /var/cache/pacman /var/lib/pacman

# Create `emacs` user
RUN useradd -ms /bin/bash emacs

# Switch to `emacs` user
ENV HOME /home/emacs
USER emacs

# Needed by `exec-path-from-shell`
ENV SHELL /bin/bash

WORKDIR /home/emacs

ENTRYPOINT ["emacs"]
