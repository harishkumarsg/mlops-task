import argparse
import json
import time

import numpy as np

from src.logger import setup_logger
from src.pipeline import run_pipeline
from src.utils import write_metrics
from src.validation import validate_config, validate_dataset

def main(argv=None):
    parser = argparse.ArgumentParser(description="MLOps Batch Job")
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args(argv)

    start_time = time.perf_counter()
    version = "v1"
    logger = None

    try:
        logger = setup_logger(args.log_file)
        logger.info("Job started")

        logger.info(
            "CLI args: input=%s config=%s output=%s log_file=%s",
            args.input,
            args.config,
            args.output,
            args.log_file,
        )

        config = validate_config(args.config)
        version = config["version"]
        np.random.seed(config["seed"])
        logger.info(
            "Config loaded and validated: seed=%s window=%s version=%s",
            config["seed"],
            config["window"],
            config["version"],
        )

        df = validate_dataset(args.input)
        logger.info("Rows loaded: %s", len(df))

        logger.info("Processing: rolling mean (window=%s)", config["window"])
        logger.info("Processing: signal generation (close > rolling_mean)")

        results = run_pipeline(df, config)

        latency_ms = int((time.perf_counter() - start_time) * 1000)

        metrics = {
            "version": config["version"],
            "rows_processed": results["rows_processed"],
            "metric": "signal_rate",
            "value": results["signal_rate"],
            "latency_ms": latency_ms,
            "seed": config["seed"],
            "status": "success"
        }

        write_metrics(args.output, metrics)

        logger.info("Metrics: %s", metrics)
        logger.info("Job completed successfully")

        print(json.dumps(metrics))
        return 0

    except Exception as e:
        error_metrics = {
            "version": version,
            "status": "error",
            "error_message": str(e)
        }

        try:
            write_metrics(args.output, error_metrics)
        except Exception:
            pass

        if logger is not None:
            logger.exception("Job failed")

        print(json.dumps(error_metrics))
        return 1

if __name__ == "__main__":
    raise SystemExit(main())