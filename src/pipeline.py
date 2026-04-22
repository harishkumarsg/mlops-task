def run_pipeline(df, config):
    window = config["window"]

    if window > len(df):
        raise ValueError("Rolling window is larger than dataset length")

    df = df.copy()
    df["rolling_mean"] = df["close"].rolling(window=window).mean()
    df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)

    valid_mask = df["rolling_mean"].notna()
    signal_rate = df.loc[valid_mask, "signal"].mean()

    return {
        "rows_processed": len(df),
        "signal_rate": round(float(signal_rate), 4),
    }