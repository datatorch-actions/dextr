# FROM python:3.6

# RUN apt-get update
# RUN apt-get install -y git libsm6 libxrender1 libfontconfig1

# WORKDIR /workspace

# COPY ./requirements_container.txt /workspace
# # Install python package dependices
# RUN pip install -r requirements_container.txt

# WORKDIR /workspace/


# COPY ./dextr_pb2.py /workspace
# COPY ./dextr_pb2_grpc.py /workspace
# COPY ./server.py /workspace
# COPY ./dextr.proto /workspace

# ENTRYPOINT [ "python", "server.py" ]

FROM python:3.8.5

RUN apt-get update
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6' -y

RUN apt install liblzma-dev

WORKDIR /workspace
COPY requirements_container.txt /workspace
RUN pip install -r requirements_container.txt
RUN python -c "from dextr.model import DextrModel; DextrModel.pascalvoc_resunet101()"
RUN pip install gunicorn==20.0.4
COPY server.py /workspace

EXPOSE 8000

WORKDIR /workspace
CMD [ "gunicorn", "-w 6", "-b 0.0.0.0:8000", "server:app" ]