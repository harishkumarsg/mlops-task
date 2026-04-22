import os

import yaml
import pandas as pd

def validate_config(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError("Invalid YAML format in config") from e
    except OSError as e:
        raise OSError(f"Unable to read config file: {e}") from e

    if not isinstance(config, dict):
        raise ValueError("Invalid config structure")

    required = ["seed", "window", "version"]
    for key in required:
        if key not in config:
            raise ValueError(f"Missing config key: {key}")

    seed = config["seed"]
    window = config["window"]
    version = config["version"]

    if not isinstance(seed, int):
        raise ValueError("Invalid config: seed must be an integer")

    if not isinstance(window, int) or window <= 0:
        raise ValueError("Invalid config: window must be a positive integer")

    if not isinstance(version, str) or not version.strip():
        raise ValueError("Invalid config: version must be a non-empty string")

    return {"seed": seed, "window": window, "version": version}

def validate_dataset(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input file not found: {path}")

    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError as e:
        raise ValueError("Input CSV is empty") from e
    except pd.errors.ParserError as e:
        raise ValueError("Invalid CSV format") from e
    except UnicodeDecodeError as e:
        raise ValueError("Unable to decode input file as text") from e

    if df.empty:
        raise ValueError("Dataset is empty")

    normalized_columns = [str(c).strip().strip('"') for c in df.columns]
    df.columns = normalized_columns

    lower_to_actual = {c.lower(): c for c in df.columns}
    if "close" not in lower_to_actual:
        raise ValueError("Missing required column: close")

    close_col = lower_to_actual["close"]
    if close_col != "close":
        df = df.rename(columns={close_col: "close"})

    df = df.copy()
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    if df["close"].isna().any():
        raise ValueError("Invalid numeric values in close column")

    return df