# Dashboard for NTU EDGE Project

A visual dashboard to analyze CSV files produced by additive manufacturing sensor systems. Built with Flask and Plotly Dash.

## Changelog

| Version | Features                                               |
| ------- | ------------------------------------------------------ |
| v1      | working base flask app + lineplot graph and data table |

See the list of issues [here](https://github.com/callistachang/dashboard-app/issues).

## Installation

Installation via Poetry:

```
$ cd dashboard_app
$ poetry install
$ poetry shell
$ flask run
```

Installation via `requirements.txt` (do this in a virtual environment):

```
$ cd dashboard_app
$ pip install -r requirements.txt
$ flask run
```

## Usage

Replace the values in `.env.example` with your own values and rename this file to `.env`. Don't commit secrets to GitHub.
