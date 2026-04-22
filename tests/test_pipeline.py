import pandas as pd

from src.pipeline import run_pipeline


def test_pipeline_basic():
    df = pd.DataFrame({"close": [1, 2, 3, 4, 5, 6]})
    config = {"window": 2}

    result = run_pipeline(df, config)

    assert result["rows_processed"] == 6
    assert 0.0 <= result["signal_rate"] <= 1.0
import pandas as pd
from src.pipeline import run_pipeline

def test_pipeline_basic():
    df = pd.DataFrame({"close": [1, 2, 3, 4, 5, 6]})
    config = {"seed": 42, "window": 2}

    result = run_pipeline(df, config)

    assert "signal_rate" in result
    assert result["rows_processed"] == 6