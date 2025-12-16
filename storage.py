import pandas as pd
import sqlite3

def load_ticks(symbol):
    con = sqlite3.connect("ticks.db")
    df = pd.read_sql(
        f"SELECT * FROM ticks WHERE symbol='{symbol}'",
        con, parse_dates=["timestamp"]
    )
    con.close()
    df.set_index("timestamp", inplace=True)
    return df

def resample(df, freq):
    return df.resample(freq).agg({
        "price": "last",
        "qty": "sum"
    }).dropna()