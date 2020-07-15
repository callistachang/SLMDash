import dash_table

def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""

    table = dash_table.DataTable(
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        sort_action='native',
        sort_mode='native',
        page_size=10
    )

    return table

def create_placeholder_df():
    import pandas as pd
    return pd.read_csv("data/sensordata.csv")