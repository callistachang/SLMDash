def pressure_and_oxygen_over_time(df):
    color1 = "#9467BD"
    color2 = "#F08B00"

    data = [
        {
            "x": df["Time"],
            "y": df["Pressure"],
            "name": "pressure",
            "line": {"color": color1},
            "type": "scattergl",
        },
        {
            "x": df["Time"],
            "y": df["Oxygen top"],
            "name": "oxygen",
            "yaxis": "y2",
            "type": "scattergl",
        },
    ]

    layout = {
        "title": "Pressure and Oxygen Over Time",
        "yaxis": {
            "title": "pressure",
            "titlefont": {"color": color1},
            "tickfont": {"color": color1},
        },
        "yaxis2": {
            "title": "oxygen",
            "overlaying": "y",
            "side": "right",
            "titlefont": {"color": color2},
            "tickfont": {"color": color2},
        },
        "height": 500,
        "width": 1000,
        "padding": 100,
    }

    return {"data": data, "layout": layout}
