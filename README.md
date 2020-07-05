# Dashboard for NTU EDGE Project

A visual dashboard to analyze CSV files produced by additive manufacturing sensor systems. Built with Flask and Plotly Dash.

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

Replace the values in `.env.example` with your own values and rename this file to `.env`.

(Don't commit secrets saved in .env files to GitHub.)

## Changelog

| Version | Features                                               |
| ------- | ------------------------------------------------------ |
| v1      | working base flask app + lineplot graph and data table |

### TODO

| Todo                                            | Status                                |
| ----------------------------------------------- | ------------------------------------- |
| base flask app                                  | :heavy_check_mark:                    |
| base plotly dash integration                    | :heavy_check_mark:                    |
| able to upload csv data; graphs respond to them | high priority                         |
| more graphs and insights                        | medium priority; waiting on teammates |
| interactive dropdown options in plotly          | medium priority                       |
| new endpoint for ML functionality               | low priority                          |

### FIXME

| Fixme                                                                                         | Potential Fixes                                                   | Status          |
| --------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | --------------- |
| dashboard loads slowly even though dataset (`data/sensordata.csv`, 104727x35) was pre-cleaned | - 'paginate' the graph and show only X number of points at one go | medium priority |
