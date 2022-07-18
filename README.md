# diff_unpack

[![Version](https://img.shields.io/docker/v/fnndsc/pl-diff_unpack?sort=semver)](https://hub.docker.com/r/fnndsc/pl-diff_unpack)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-diff_unpack)](https://github.com/FNNDSC/pl-diff_unpack/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-diff_unpack/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-diff_unpack/actions/workflows/ci.yml)

`pl-diff_unpack` is a [_ChRIS_](https://chrisproject.org/)
_ds_ plugin that wraps around the Diffusion Toolkit app `diff_unpack`. This app consumes DICOMs as input files and creates NIfTI or Analyze conversions as output files. The ChRIS plugin version effectively extends the original app to operate across multiple directory spaces.

## Abstract

Little more than simple dockerized wrapper about the image conversion tool `diff_unpack`, this plugin allows multi-directory in the input space and will run `diff_unpack` on each input directory. Essentially, `diff_unpack` converts input DICOM format files into ANALYZE or NIfTI format. While part of a diffusion imaging process, this conversion application is relatively generic and is useful in its own right. For more information on the actual tool, refer [here](http://trackvis.org/dtk/?subsect=workflow).

 "Ruopeng Wang, Van J. Wedeen, TrackVis.org, Martinos Center for Biomedical Imaging, Massachusetts General Hospital, ISMRM Proc. Intl. Soc. Mag. Reson. Med. 15 (2007) 3720"

## Installation

`pl-diff_unpack` is a _[ChRIS](https://chrisproject.org/) plugin_ about the `diff_unpack` application of Diffusion Toolkit. It is typically deployed as part of the ChRIS Store:

[![Get it from chrisstore.co](https://ipfs.babymri.org/ipfs/QmaQM9dUAYFjLVn3PpNTrpbKVavvSTxNLE5BocRCW1UoXG/light.png)](https://chrisstore.co/plugin/pl-diff_unpack)

Alternatively, you can get a docker image here:

```shell
docker pull fnndsc/pl-diff_unpack:latest
```

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

### Using a local docker image

If during development you would like to run your _local_ image via `singularity` you need to deploy a local docker registry, push your container to that, and use this to generate the `apptainer`:

```shell
docker run -d -p 5000:5000 --restart=always --name registry registry:2
docker tag localhost/fnndsc/pl-diff_unpack localhost:5000/fnndsc/pl-diff_unpack
docker push localhost:5000/fnndsc/pl-diff_unpack
APPTAINER_NOHTTPS=1 singularity exec docker://localhost:5000/fnndsc/pl-diff_unpack diff_unpack --help /tmp /tmp/ 
```

## Examples

`diff_unpack` requires two positional arguments: a directory containing input data, and a directory where to create output data. First, create the input directory and move input data into it. This application as part of the Diffusion Toolik

```shell
mkdir incoming/ outgoing/
mv someDICOM.dcm moreDICOM.dcm incoming/
singularity exec docker://fnndsc/pl-diff_unpack:latest diff_unpack incoming/ outgoing/
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

Mount the source code `diff_unpack.py` into a container to try out changes without rebuild.

```shell
docker run --rm -it --userns=host -u $(id -u):$(id -g) \
    -v $PWD/diff_unpack.py:/usr/local/lib/python3.10/site-packages/diff_unpack.py:ro \
    -v $PWD/init:/usr/local/lib/python3.10/site-packages/init:ro \
    -v $PWD/job:/usr/local/lib/python3.10/site-packages/job:ro \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw -w /outgoing \
    localhost/fnndsc/pl-diff_unpack diff_unpack /incoming /outgoing
```

### Testing

Run unit tests using `pytest`.
It's recommended to rebuild the image to ensure that sources are up-to-date.
Use the option `--build-arg extras_require=dev` to install extra dependencies for testing.

```shell
docker build -t localhost/fnndsc/pl-diff_unpack:dev --build-arg extras_require=dev .
docker run --rm -it localhost/fnndsc/pl-diff_unpack:dev pytest
```

_-30-_