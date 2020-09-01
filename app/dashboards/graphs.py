from .constants import TEMP_COLUMNS, COLUMNS_TO_KEEP

# 9 colors for 9 columns
COLORS = [
    "#e41a1c",
    "#377eb8",
    "#4daf4a",
    "#984ea3",
    "#ff7f00",
    "#ffff33",
    "#a65628",
    "#f781bf",
    "#999999",
]

COLUMNS = COLUMNS_TO_KEEP[:]
COLUMNS.remove("Time")
COLOR_MAPPER = dict(zip(COLUMNS, COLORS))


def main_graph(df):
    print("main_graph()")
    columns = [col for col in df.columns if not col in TEMP_COLUMNS]

    data = [
        {
            "x": df["Time"],
            "y": df[columns[i]],
            "name": columns[i],
            "line": {"color": COLOR_MAPPER[columns[i]]},
            "type": "scattergl",
        }
        for i in range(len(columns))
    ]

    layout = {
        "title": f"{', '.join(columns)} Over Time",
        "xaxis": {"title": "Time"},
        "yaxis": {"title": ", ".join(columns)},
    }

    return {"data": data, "layout": layout}
