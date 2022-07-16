# Python version can be changed, e.g.
# FROM python:3.8
# FROM docker.io/fnndsc/conda:python3.10.2-cuda11.6.0
FROM docker.io/python:3.10.5-slim-buster

LABEL org.opencontainers.image.authors="FNNDSC <rudolph.pienaar@childrens.harvard.edu>" \
      org.opencontainers.image.title="diff_unpack" \
      org.opencontainers.image.description="A ChRIS DS plugin that is a thin wrapper about diff_unpack (part of TrackVis, original author Ruopeng Wang)"

WORKDIR /usr/local/src/pl-diff_unpack

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ARG extras_require=none
RUN pip install ".[${extras_require}]"

CMD ["diff_unpack", "--help"]
