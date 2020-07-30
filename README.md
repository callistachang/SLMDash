# Dashboard for NTU EDGE Project

A visual dashboard to analyze CSV files produced by additive manufacturing sensor systems. Built with Flask and Plotly Dash.

## Installation

Installation via Poetry:

```
$ cd dashboard-app
$ poetry install
$ poetry shell
$ flask run
```

Installation via `requirements.txt` (recommended to do this in a virtual environment):

```
$ cd dashboard-app
$ pip install -r requirements.txt
$ flask run
```

## Usage

Replace the values in `.env.example` with your own values and rename this file to `.env`.

Run `poetry run black .` before committing to the repo to standardize the code formatting.

## Changelog

| Version | Features                                               |
| ------- | ------------------------------------------------------ |
| v1      | working base flask app + lineplot graph and data table |
| v2      | upload csv functionality + fixed slow loading          |

See the list of issues [here](https://github.com/callistachang/dashboard-app/issues).
