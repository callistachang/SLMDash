import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest


def detect_anomalies(input_df, col, t1, t2):
    mod = IsolationForest(
        n_estimators=100,
        max_samples="auto",
        max_features=1.0,
        bootstrap=False,
        n_jobs=-1,
        random_state=42,
        verbose=1,
    )
    col_df = input_df.loc[:, col].values.reshape(-1, 1)
    mod.fit(col_df)
    df = pd.DataFrame()
    df["Time"] = input_df["Time"]
    df["score"] = mod.decision_function(col_df)
    df["actual"] = col_df
    df["anomaly"] = mod.predict(col_df)
    df, anomalies = classify_anomalies(df, t1, t2)
    return df


def classify_anomalies(df, t1, t2):
    df = df.sort_values(by="Time", ascending=True)
    # Categorise anomalies as 0 - no anomaly, 2 - anomaly
    df["anomaly"].loc[df["actual"].between(t1, t2) == False] = 2
    df["anomaly"].loc[(df["anomaly"] == 1) & (df["actual"].between(t1, t2) == True)] = 0
    df["anomaly"].loc[
        (df["anomaly"] == -1) & (df["actual"].between(t1, t2) == True)
    ] = 0
    df["anomaly"].loc[
        (df["anomaly"] == -1) & (df["actual"].between(t1, t2) == False)
    ] = 2
    # Shift actuals by one timestamp to find the percentage chage between current and previous data point
    df["shift"] = df["actual"].shift(-1)
    df["percentage_change"] = ((df["actual"] - df["shift"]) / df["actual"]) * 100
    df["percentage_change"].loc[df["percentage_change"].isnull()] = 0
    dates = df.Time
    # identify the anomaly points and create a array of its values for plot
    bool_array = abs(df["anomaly"]) > 0
    actuals = df["actual"][: len(bool_array)]
    anomaly_points = bool_array * actuals
    df["anomaly_points"] = anomaly_points
    anomalies = pd.DataFrame()
    anomalies["Time"] = df["Time"][4000:]
    anomalies["percentage_change"] = df["percentage_change"][4000:]
    anomalies["anomaly_points"] = df["anomaly_points"][4000:]
    anomalies = anomalies[anomalies["anomaly_points"] != 0]
    df["anomaly_points"].loc[df["anomaly_points"] == 0] = np.nan
    print(anomalies)
    return df, anomalies

