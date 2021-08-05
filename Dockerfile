# This Dockerfile creates an enviroment / dependancies needed to run the 
# cubit_docker package.

# You will need to have you license file saved as license.lic in the same folder
# as this Dockerfile when building

# To build this Dockerfile into a docker image:
# docker build -t cubit_docker .

# To run the resulting Docker image:
# docker run -it cubit_docker


# FROM continuumio/miniconda3:4.10.3 as dependencies
# FROM continuumio/miniconda3:4.9.2 as dependencies

FROM ubuntu:20.04


ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    PATH=/opt/openmc/bin:$PATH \
    LD_LIBRARY_PATH=/opt/openmc/lib:$LD_LIBRARY_PATH \
    CC=/usr/bin/mpicc CXX=/usr/bin/mpicxx \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get upgrade -y

RUN apt-get install -y libgl1-mesa-glx \
                       libgl1-mesa-dev \
                       libglu1-mesa-dev \
                       freeglut3-dev \
                       libosmesa6 \
                       libosmesa6-dev \
                       libgles2-mesa-dev \
                       curl \
                       wget && \
                       apt-get clean

# download cubit
RUN wget -O coreform-cubit-2021.5.deb https://f002.backblazeb2.com/file/cubit-downloads/Coreform-Cubit/Releases/Linux/Coreform-Cubit-2021.5%2B15962_5043ef39-Lin64.deb

# install dependencies
RUN apt-get install -y libx11-6 
RUN apt-get install -y libxt6 
RUN apt-get install -y libgl1
RUN apt-get install -y libglu1-mesa
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y libxcb-icccm4 
RUN apt-get install -y libxcb-image0 
RUN apt-get install -y libxcb-keysyms1 
RUN apt-get install -y libxcb-render-util0 
RUN apt-get install -y libxkbcommon-x11-0 
RUN apt-get install -y libxcb-randr0 
RUN apt-get install -y libxcb-xinerama0

# install cubit
RUN dpkg -i coreform-cubit-2021.5.deb


# makes a python file and trys to import cubit
# RUN printf 'import sys\nsys.path.append("/opt/Coreform-Cubit-2021.5/bin/")\nimport cubit\ncubit.init([])\n' >> test_cubit_import.py

# writes a non commercial license file
RUN printf 'Fri May 28 2021' >> /opt/Coreform-Cubit-2021.5/bin/licenses/license.lic



RUN wget https://github.com/svalinn/Cubit-plugin/releases/download/0.1.0/svalinn-plugin_ubuntu-20.04_cubit_2021.5.tgz
RUN tar -xzvf svalinn-plugin_ubuntu-20.04_cubit_2021.5.tgz -C /opt/Coreform-Cubit-2021.5

# FROM dependencies as final


COPY setup.py setup.py
COPY README.md README.md
COPY run_tests.sh run_tests.sh
COPY tests tests/
COPY examples examples/
COPY cad_to_h5m cad_to_h5m/




ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update

RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# install python 3.8
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-py38_4.10.3-Linux-x86_64.sh -b \
    && rm -f Miniconda3-py38_4.10.3-Linux-x86_64.sh 

RUN conda --version


RUN python setup.py install
