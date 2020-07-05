# Dashboard for NTU EDGE Project

A visual dashboard to analyze CSV files produced by additive manufacturing sensor systems. Built with Flask and Plotly Dash.

## Installation

Installation via Poetry:

```
$ cd flaskproject
$ poetry install
$ poetry shell
$ flask run
```

Installation via `requirements.txt` (better to do this inside a virtual environment):

```
$ cd flaskproject
$ pip install -r requirements.txt
$ flask run
```

## Usage

Replace the values in `.env.example` with your own values and rename this file to `.env`.

(Don't commit secrets saved in .env files to GitHub!!)

## Changelog

| Version | Features                                               |
| ------- | ------------------------------------------------------ |
| v1      | working base flask app + lineplot graph and data table |

<!-- Working base Flask application.<br>Plotly Dash graph featuring a lineplot of over time. | -->

**TODO**

- Function to upload CSV files and have the graphs react dynamically to the new dataset.
- More types of graphs and insights - waiting on my teammates for more ideas.
- Endpoint to run image files through machine learning models.

**FIXME**

- Dashboard loads very slowly even though the I pre-cleaned the dataset (`sensordata.csv`, 104727x35).
