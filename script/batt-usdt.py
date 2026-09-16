import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, TextIO, Tuple

TEMPDATA = (Path(__file__).parent.parent / "temp_data").resolve()
CHARTS = (Path(__file__).parent.parent / "assets" / "chart").resolve()

batt_percent_re = re.compile(r"^\[(.*)\%\]", flags=re.MULTILINE)


def preprocess(f: TextIO) -> List[Tuple[datetime, float]]:
    end_time = datetime.fromisoformat("2026-09-16T16:10:00.000000+08:00")
    dt = timedelta(minutes=1)
    values: List[float] = []
    for m in batt_percent_re.finditer(f.read()):
        g = m.groups()
        if len(g) != 1:
            continue
        values.append(float(g[0]))
    if not values:
        return []
    start_time = end_time - dt * (len(values) - 1)
    return [(start_time + i * dt, val) for i, val in enumerate(values)]


def data_to_series(data: List[Tuple[datetime, float]]) -> dict:
    base = {
        "xAxis": {
            "type": "time",
            "name": "日期时间",
            "minInterval": 60 * 1000,  # 1 min
            "splitArea": {"show": True},
            "splitLine": {"show": True, "lineStyle": {"type": "dashed"}},
        },
        "series": [
            {
                "name": "BATT/USDT",
                "type": "line",
                "showSymbol": False,
                "data": [],
            }
        ],
    }
    for dp in data:
        date_str = dp[0].strftime("%Y-%m-%d %H:%M")
        # base["xAxis"][0]["data"].append(date_str)
        base["series"][0]["data"].append([date_str, dp[1]])
    return base


def main():
    data_batt: List[Tuple[datetime, float]] = []
    with open(TEMPDATA / "batt_usdt.txt", "r") as f:
        data_batt = preprocess(f)
    with open(CHARTS / "the-art-of-medication-schedule-data-3.json", "w") as f:
        dp = data_to_series(data_batt)
        json.dump(dp, f)
    pass


if __name__ == "__main__":
    main()
