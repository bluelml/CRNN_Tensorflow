FROM tensorflow/tensorflow:1.3.0-gpu-py3

RUN rm -rf /var/lib/apt/lists/*
RUN apt update && \
    apt install -y --no-install-recommends \
        python3-tk \
        vim \
        ssh \
        git && \
    rm -rf /var/lib/apt/lists/* 

#ADD . /app
RUN mkdir /project

COPY docker/requirements.txt /requirements.txt

WORKDIR /project

#RUN pip3 install -r /app/docker/requirements.txt
RUN pip3 install -r /requirements.txt

ENV PYTHONPATH=/project

# TensorBoard
EXPOSE 6006

# JupyterLab
EXPOSE 8888

CMD ["/usr/local/bin/jupyter-lab", "--allow-root", "--no-browser"]

