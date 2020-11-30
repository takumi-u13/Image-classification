FROM ubuntu:latest 
# update
RUN apt-get -y update && apt-get install -y \
libsm6 \
libxext6 \
libxrender-dev \
libglib2.0-0 \
sudo \
wget \
vim

#install anaconda3
WORKDIR /opt
# download anaconda package and install anaconda
# archive -> https://repo.continuum.io/archive/
RUN wget https://repo.continuum.io/archive/Anaconda3-2020.02-Linux-x86_64.sh && \
	sh /opt/Anaconda3-2020.02-Linux-x86_64.sh -b -p /opt/anaconda3 && \
	rm -f Anaconda3-2020.02-Linux-x86_64.sh
# set path
ENV PATH /opt/anaconda3/bin:$PATH

# update pip and install packages
RUN pip install --upgrade pip && \
	pip install jupyter-contrib-nbextensions && \
	pip install jupyter-nbextensions-configurator && \
	pip install tensorflow && \
	pip install flickrapi  && \
    pip install pillow && \
    pip install sklearn && \
    pip install keras && \
    pip install Flask

RUN mkdir /work
WORKDIR /work

CMD ["python", "predict_file.py"]