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
    pred = mod.predict(col_df)
    anomaly = pd.DataFrame()
    anomaly["Time"] = input_df["Time"]

    # Find decision function to find the score and classify anomalies
    anomaly["score"] = mod.decision_function(col_df)
    anomaly["actual"] = col_df
    anomaly["anomaly"] = pred

    # Categorise anomalies as 0-no anomaly, 2-anomaly
    anomaly["anomaly"].loc[(anomaly["anomaly"] == 1)] = 0
    anomaly["anomaly"].loc[(anomaly["anomaly"] == -1)] = 2
    anomaly["anomaly"].loc[anomaly["actual"].between(t1, t2) == False] = 2
    anomaly["anomaly"].loc[
        ((anomaly["anomaly"] == 0) | (anomaly["anomaly"] == 2))
        & (anomaly["actual"].between(t1, t2) == True)
    ] = 0
    anomaly["anomaly"].loc[
        (anomaly["anomaly"] == 2) & (anomaly["actual"].between(t1, t2) == False)
    ] = 2
    anomaly = anomaly[anomaly["anomaly"] != 0]
    return anomaly["Time"]

