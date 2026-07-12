import os
import json
from datetime import datetime, timezone

def write_json_file(data: dict, file_path: str) -> None:
    # 'with open' acts as a context manager; it automatically closes the file 
    # safely when the block finishes, preventing memory leaks or data corruption.
    # "w" is write mode, "r" for read mode
    data["ingestion_timestamp"] = datetime.now(timezone.utc).isoformat()
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)