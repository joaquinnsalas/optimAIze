FROM python:3.11.7-slim
LABEL maintainer="Joaquin Salas <jsalas2002@tamu.edu>"
LABEL version="1.0"
LABEL description="Data Analyst"

RUN apt-get update -y
RUN apt-get install -y gcc
RUN apt-get install -y build-essential libpq-dev
RUN apt-get install -y graphviz

RUN pip install --upgrade pip

# Installing packages
RUN pip install \
    numpy==1.26.4 \
    pandas==2.2.0 \
    pyarrow==16.0.0\
    seaborn==0.13.2 \ 
    jupyter==1.0.0 \  
    scikit-learn==1.4.0 \ 
    statsmodels==0.14.1 \
    matplotlib==3.8.4

WORKDIR /home/notebooks/

CMD jupyter notebook --no-browser --allow-root --ip 0.0.0.0
