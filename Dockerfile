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
COPY dextr.txt /workspace
RUN pip install -r dextr.txt
RUN python -c "from dextr.model import DextrModel; DextrModel.pascalvoc_resunet101()"
COPY image.jpg /workspace
COPY test.py /workspace

ENTRYPOINT [ "python", "test.py" ]