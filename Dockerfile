FROM centos:7

LABEL authors="Andres Anania <aanania@lsst.org>"

# install required software
RUN yum -y --enablerepo=extras install epel-release \
  gsl \
  unzip \
  wget \
  git \
  tk \
  tk-devel \
  swig \
  ncurses-libs \
  xterm \
  xorg-x11-fonts-misc \
  java-1.8.0-openjdk-devel \
  boost-python \
  boost-python-devel \
  maven \
  python-devel \
  python-pip \
  python-wheel \
  gnome-terminal \
  mariadb \
  mariadb-server \
  mysql-devel \
  nano && \
  yum clean all

RUN yum groupinstall -y "Development Tools" "Development Libraries" && \
  yum clean all

# install python3
COPY python3-to-install.tgz .
RUN tar -zxvf python3-to-install.tgz && rm python3-to-install.tgz
RUN cd Python-3.6.3 && make install

COPY ./requirements.txt /home/docker/requirements.txt
RUN pip3 install -r /home/docker/requirements.txt

WORKDIR "/home/docker/"
RUN git clone https://github.com/aanania/bokeh_test.git

COPY run.sh /home/docker/lsst/run.sh

RUN chmod +x /home/docker/lsst/run.sh

ENTRYPOINT /home/docker/lsst/run.sh
