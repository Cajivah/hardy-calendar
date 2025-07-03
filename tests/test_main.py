import os
import json
from datetime import datetime
from src.hardy_calendar.orchestrator import save_plans_to_file

def test_save_plans_to_file(tmp_path):
    # Prepare test data
    plans = {
        datetime(2025, 7, 3): "desc1",
        datetime(2025, 7, 4): "desc2"
    }
    file_path = tmp_path / "plans.json"
    # Patch open to write to tmp_path
    orig_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        save_plans_to_file(plans)
        assert os.path.exists("plans.json")
        with open("plans.json", encoding="utf-8") as f:
            data = json.load(f)
        # Keys should be stringified datetimes
        assert set(data.keys()) == {"2025-07-03 00:00:00", "2025-07-04 00:00:00"}
        assert data["2025-07-03 00:00:00"] == "desc1"
        assert data["2025-07-04 00:00:00"] == "desc2"
    finally:
        os.chdir(orig_cwd)
