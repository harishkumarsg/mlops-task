import json
from pathlib import Path


def write_metrics(path, data):
    output_path = Path(path)
    if str(output_path.parent) not in (".", ""):
        output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
import json

def write_metrics(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)