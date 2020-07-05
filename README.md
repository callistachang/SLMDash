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

Installation via `requirements.txt` (do this in a virtual environment):

```
$ cd dashboard-app
$ pip install -r requirements.txt
$ flask run
```

## Usage

Replace the values in `.env.example` with your own values and rename this file to `.env`.

(Don't commit secrets saved in .env files to GitHub.)

## Changelog

| Version | Features                                               |
| ------- | ------------------------------------------------------ |
| v1      | working base flask app + lineplot graph and data table |

## TODO

- Function to upload CSV files, then have the graphs react dynamically to the new dataset.
- More types of graphs and insights - waiting on my teammates for more ideas.
- Endpoint to run image files through machine learning models.
- Should come up with an actual name for this project and rename some of the folders.

**FIXME**

- Dashboard loads very slowly even though the the dataset was pre-cleaned (`sensordata.csv`, 104727x35).
