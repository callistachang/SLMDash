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

Run `black .` before committing to the repo to standardize code formatting.

## Changelog

| Version | Features                                                            |
| ------- | ------------------------------------------------------------------- |
| v1      | working flask app + static data dashboard                           |
| v2      | upload csv functionality on the data dashboard + fixed slow loading |
| v3      | index page + skeletons for each of the 4 sections                   |

See the list of issues [here](https://github.com/callistachang/dashboard-app/issues).

## Contributing Members

- Callista Rossary Chang
- Wang Yi
- Swati Shet
- Xiao Yang
