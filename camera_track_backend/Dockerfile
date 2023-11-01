FROM python:3.10

ENV PYTHONUNBUFFERED=1
# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
      bzip2 \
      g++ \
      git \
      graphviz \
      libgl1-mesa-glx \
      libhdf5-dev \
      openmpi-bin \
      wget \
      python3-tk && \
    rm -rf /var/lib/apt/lists/*
RUN apt-get install default-libmysqlclient-dev
RUN pip install poetry  
#RUN mkdir -p /
#COPY . /

#WORKDIR /

#RUN poetry install
#EXPOSE 8000
#CMD ["poetry", "run", "python", "manage.py", "runserver","0.0.0.0:8000"]
