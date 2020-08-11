from .constants import TEMP_COLUMNS


def main_graph(df):
    columns = [col for col in df.columns if not col in TEMP_COLUMNS]

    data = [
        {"x": df["Time"], "y": df[col], "name": col, "type": "scattergl"}
        for col in columns
    ]

    layout = {
        "title": f"{', '.join(columns)} Over Time",
        "xaxis": {"title": "Time"},
        "yaxis": {"title": ", ".join(columns),},
    }

    return {"data": data, "layout": layout}
