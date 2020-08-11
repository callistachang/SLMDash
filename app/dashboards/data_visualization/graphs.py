from .constants import TEMP_COLUMNS

# 9 colors
colors = [
    "#577590",
    "#E5A9A9",
    "#F3CA40",
    "#00BD9D",
    "#54DEFD",
]


def main_graph(df):
    columns = [col for col in df.columns if not col in TEMP_COLUMNS]

    data = [
        {
            "x": df["Time"],
            "y": df[columns[i]],
            "name": columns[i],
            "line": {"color": colors[i]},
            "type": "scattergl",
        }
        for i in range(len(columns))
    ]

    layout = {
        "title": f"{', '.join(columns)} Over Time",
        "xaxis": {"title": "Time"},
        "yaxis": {"title": ", ".join(columns)}
    }

    return {"data": data, "layout": layout}
