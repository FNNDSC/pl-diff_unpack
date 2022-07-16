# diff_unpack

[![Version](https://img.shields.io/docker/v/fnndsc/pl-diff_unpack?sort=semver)](https://hub.docker.com/r/fnndsc/pl-diff_unpack)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-diff_unpack)](https://github.com/FNNDSC/pl-diff_unpack/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-diff_unpack/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-diff_unpack/actions/workflows/ci.yml)

`pl-diff_unpack` is a [_ChRIS_](https://chrisproject.org/)
_ds_ plugin which takes in ...  as input files and
creates ... as output files.

## Abstract

...

## Installation

`pl-diff_unpack` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can
run from either within _ChRIS_ or the command-line.

[![Get it from chrisstore.co](https://ipfs.babymri.org/ipfs/QmaQM9dUAYFjLVn3PpNTrpbKVavvSTxNLE5BocRCW1UoXG/light.png)](https://chrisstore.co/plugin/pl-diff_unpack)

## Local Usage

To get started with local command-line usage, use [Apptainer](https://apptainer.org/)
(a.k.a. Singularity) to run `pl-diff_unpack` as a container:

```shell
singularity exec docker://fnndsc/pl-diff_unpack diff_unpack [--args values...] input/ output/
```

To print its available options, run:

```shell
singularity exec docker://fnndsc/pl-diff_unpack diff_unpack --help
```

## Examples

`diff_unpack` requires two positional arguments: a directory containing
input data, and a directory where to create output data.
First, create the input directory and move input data into it.

```shell
mkdir incoming/ outgoing/
mv some.dat other.dat incoming/
singularity exec docker://fnndsc/pl-diff_unpack:latest diff_unpack [--args] incoming/ outgoing/
```

## Development

Instructions for developers.

### Building

Build a local container image:

```shell
docker build -t localhost/fnndsc/pl-diff_unpack .
```

### Get JSON Representation

Run [`chris_plugin_info`](https://github.com/FNNDSC/chris_plugin#usage)
to produce a JSON description of this plugin, which can be uploaded to a _ChRIS Store_.

```shell
docker run --rm localhost/fnndsc/pl-diff_unpack chris_plugin_info > chris_plugin_info.json
```

### Local Test Run

Mount the source code `diff_unpack.py` into a container to test changes without rebuild.

```shell
docker run --rm -it --userns=host -u $(id -u):$(id -g) \
    -v $PWD/diff_unpack.py:/usr/local/lib/python3.10/site-packages/diff_unpack.py:ro \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw -w /outgoing \
    localhost/fnndsc/pl-diff_unpack diff_unpack /incoming /outgoing
```
