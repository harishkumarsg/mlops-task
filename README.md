# MLOps Batch Pipeline

## Features
- Deterministic runs via config + seed
- Structured logging
- Error-safe execution
- Dockerized pipeline
- Unit testing included

## Run Locally
Install dependencies:

pip install -r requirements.txt

Run (required CLI):

python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

Notes:
- Rolling mean is computed with the configured `window`.
- The first `window-1` rows have no rolling mean (NaN) and are excluded from `signal_rate`.

## Run Tests
make test

## Docker
docker build -t mlops-task 
docker run --rm mlops-task

Example metrics.json:

{
	"version": "v1",
	"rows_processed": 10000,
	"metric": "signal_rate",
	"value": 0.499,
	"latency_ms": 127,
	"seed": 42,
	"status": "success"
}

## CLI Usage

python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

## Sample Output

{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4991,
  "latency_ms": 28,
  "seed": 42,
  "status": "success"
}
