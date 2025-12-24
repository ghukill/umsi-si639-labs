# umsi-si639-labs

Repository for University of Michigan, School of Information, SI639 - Web Archiving labs.

## Installation

1- [Install uv](https://docs.astral.sh/uv/getting-started/installation/) for python environment management.

Check that `uv` is installed correctly:
```shell
uv --version

# should see something like
# uv 0.9.18 (0cee76417 2025-12-16)
```

2- Clone this repository: https://github.com/ghukill/umsi-si639-labs

3- Create python virtual environment:
```shell
uv venv .venv --python 3.12
```

4- Install dependencies:
```shell
uv sync
```

## Labs

Labs can be found at [/labs](labs).