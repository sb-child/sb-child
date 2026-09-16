import json
import math
import re
from dataclasses import dataclass, field
from datetime import datetime, time, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Dict, List, TextIO, Tuple

import numpy as np
from scipy.signal import find_peaks

TEMPDATA = (Path(__file__).parent.parent / "temp_data").resolve()
CHARTS = (Path(__file__).parent.parent / "assets" / "chart").resolve()


def fmt_float(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".")


class Application(Enum):
    Other = "-"  # 未分类
    Hypnotic = "安眠"
    Antidepressants = "抗抑郁"
    Sedative = "镇静"
    Anxiolytics = "抗焦虑"
    Estrogen = "雌激素"
    Antiandrogen = "抗雄激素"


class Classification(Enum):
    Other = "-"  # 未分类
    Common = "常用药"
    BZDs = "苯二氮䓬类"
    ZDurgs = "Z药"
    Alcohol = "酒精"
    Supplements = "补充剂"
    MoodStabilizer = "心境稳定剂"
    Stimulants = "兴奋剂"
    SSRIs = "SSRI抗抑郁药"
    SNRIs = "SNRI抗抑郁药"
    SARIs = "SARI抗抑郁药"
    NDRIs = "NDRI抗抑郁药"
    NaSSAs = "NaSSA抗抑郁药"
    ORAs = "食欲素受体拮抗剂"
    SNIs = "交感神经抑制剂"  # Sympathetic nerve inhibitors
    Antihistamine = "抗组胺药"
    Antipsychotic = "抗精神病药"
    HRT = "HRT类"

    def other(self) -> bool:
        return self == Classification.Other


def classification(actions: List[Action]):
    drank = re.compile(r"喝.*酒", flags=re.MULTILINE)
    for ac in actions:
        _t = ac.dt
        for i, ev in enumerate(ac.events):
            if type(ev) is Event:
                q_mg = ev.get_quantity("mg")

                if any(s in ev.name for s in ["ev", "雌"]):
                    ev.classification = Classification.HRT
                    ev.applications.append(Application.Estrogen)

                if any(s in ev.name for s in ["cpa"]):
                    ev.classification = Classification.HRT
                    ev.applications.append(Application.Antiandrogen)

                if any(s in ev.name for s in ["碳酸锂", "丙戊酸钠", "丙戊酸镁"]):
                    ev.classification = Classification.MoodStabilizer

                if any(
                    s in ev.name for s in ["佐匹克隆", "思诺思", "唑吡坦", "扎来普隆"]
                ):
                    ev.classification = Classification.ZDurgs
                    ev.applications.append(Application.Hypnotic)

                if any(s in ev.name for s in ["唑仑", "西泮", "地达西尼"]):
                    ev.classification = Classification.BZDs
                    if "地达西尼" in ev.name:
                        ev.applications.append(Application.Hypnotic)
                    else:
                        ev.applications.append(Application.Anxiolytics)
                        ev.applications.append(Application.Sedative)

                if any(s in ev.name for s in ["vc", "维生素", "鱼油", "葡萄糖"]):
                    ev.classification = Classification.Supplements

                if any(s in ev.name for s in ["曲唑酮"]):
                    ev.classification = Classification.SARIs
                    if q_mg is not None and q_mg <= 150:
                        ev.applications.append(Application.Hypnotic)
                        ev.applications.append(Application.Sedative)
                    else:
                        ev.applications.append(Application.Antidepressants)

                if any(s in ev.name for s in ["米氮平"]):
                    ev.classification = Classification.SARIs
                    if q_mg is not None and q_mg <= 15:
                        ev.applications.append(Application.Hypnotic)
                        ev.applications.append(Application.Sedative)
                    else:
                        ev.applications.append(Application.Antidepressants)

                if any(s in ev.name for s in ["安非他酮"]):
                    ev.classification = Classification.NDRIs
                    ev.applications.append(Application.Antidepressants)

                if any(s in ev.name for s in ["文拉法辛"]):
                    ev.classification = Classification.SNRIs
                    ev.applications.append(Application.Antidepressants)

                if any(s in ev.name for s in ["喹硫平"]):
                    ev.classification = Classification.Antipsychotic
                    if q_mg is not None and q_mg <= 150:
                        ev.applications.append(Application.Hypnotic)
                        ev.applications.append(Application.Sedative)
                    else:
                        pass  # todo

                if any(s in ev.name for s in ["莱博雷生"]):
                    ev.classification = Classification.ORAs
                    ev.applications.append(Application.Hypnotic)

                if any(s in ev.name for s in ["异丙嗪"]):
                    ev.classification = Classification.Antihistamine
                    ev.applications.append(Application.Hypnotic)
                    ev.applications.append(Application.Sedative)

                if any(s in ev.name for s in ["苯海拉明", "茶苯海明"]):
                    ev.classification = Classification.Antihistamine
                    ev.applications.append(Application.Sedative)

                if any(s in ev.name for s in ["西替利嗪", "氯雷他定"]):
                    ev.classification = Classification.Antihistamine
                    pass  # todo

                if any(s in ev.name for s in ["哌甲酯"]):
                    ev.classification = Classification.Stimulants
                    pass  # todo

                if "头孢克污" in ev.name:
                    ev.name = ev.name.replace("头孢克污", "头孢克肟")

                if any(
                    s in ev.name
                    for s in [
                        "铝碳酸镁",
                        "布洛芬",
                        "奥美拉唑",
                        "头孢克肟",
                        "板蓝根",
                        "对乙酰氨基酚",
                        "蒙脱石散",
                        "氨酚烷胺",
                        "肠炎宁",
                    ]
                ):
                    ev.classification = Classification.Common
                    pass  # todo

                pass
            elif type(ev) is Notice:
                if len(drank.findall(ev.msg)) > 0:
                    ev.classification = Classification.Alcohol
                if any(s in ev.msg for s in ["vc", "维生素", "鱼油", "葡萄糖"]):
                    ev.classification = Classification.Supplements
                if any(s in ev.msg for s in ["护肝片"]):
                    ev.classification = Classification.Common
                if any(s in ev.msg for s in ["右美托咪定"]):
                    ev.classification = Classification.SNIs
                    ev.applications.append(Application.Hypnotic)
                    ev.applications.append(Application.Sedative)

                # 这里的 左/右 指的是 日雌打哪个腿
                # 这里的 贴上 指的是雌激素贴片
                if (
                    any(s in ev.msg for s in ["ev", "雌", "左", "右", "贴上"])
                    and ev.classification.other()
                ):
                    ev.classification = Classification.HRT
                    ev.applications.append(Application.Estrogen)

                # cpa: 醋酸环丙孕酮
                if any(s in ev.msg for s in ["cpa"]) and ev.classification.other():
                    ev.classification = Classification.HRT
                    ev.applications.append(Application.Antiandrogen)
            else:
                pass
            pass
    pass


@dataclass
class Event:
    name: str
    quantity: float
    unit: str
    classification: Classification = Classification.Other
    applications: List[Application] = field(default_factory=list)

    def __repr__(self) -> str:
        cl = str(self.classification.value)
        ap = "|".join([str(v.value) for v in self.applications])
        return f"Cl[{cl}] Ap[{ap}] *{self.name} {self.q()}"

    def q(self) -> str:
        q = self.get_quantity("mg")
        g = (
            f"{fmt_float(self.quantity)}{self.unit}"
            if q is None
            else f"{fmt_float(q)}mg"
        )
        return g

    def get_quantity(self, target_unit: str) -> float | None:
        current_u = self.unit.strip().lower()
        target_u = target_unit.strip().lower()
        if target_u == "t" or current_u == "t":
            return None
        if current_u == target_u:
            return self.quantity
        unit_factors = {
            "g": 1.0,
            "mg": 0.001,
        }
        if current_u in unit_factors and target_u in unit_factors:
            quantity_in_g = self.quantity * unit_factors[current_u]
            return quantity_in_g / unit_factors[target_u]
        return None


@dataclass
class Notice:
    msg: str
    classification: Classification = Classification.Other
    applications: List[Application] = field(default_factory=list)

    def __repr__(self) -> str:
        cl = str(self.classification.value)
        ap = "|".join([str(v.value) for v in self.applications])
        return f"Cl[{cl}] Ap[{ap}] !{self.msg}"


@dataclass
class Action:
    dt: datetime
    events: List[Event | Notice]

    def __repr__(self) -> str:
        dt = str(self.dt)
        if len(self.events) == 0:
            return f"@{dt}: no events"
        buf = "\n"
        for e in self.events:
            buf += f"  - {str(e)}\n"
        return f"@{dt}:{buf}"


def preprocess(f: TextIO) -> List[Action]:
    actions = []
    for line in f.readlines():
        line = line.strip()
        m = re.match(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s+(.+)$", line)
        if m is None:
            continue
        dt, content = m.group(1), m.group(2)
        dt = datetime.strptime(dt, "%Y-%m-%d %H:%M")
        dt = dt.replace(tzinfo=timezone(timedelta(hours=8)))
        items = re.split(r"[,，]\s*", content)
        events = []
        for item in items:
            ma = re.match(r"(\S+)\s+(\d+(?:\.\d+)?)(mg|g|片|ml|t)", item)
            mb = re.match(r"(\d+(?:\.\d+)?)片(\S+)", item)
            if ma:
                # print(f"{dt} | {ma.group(1)} | {ma.group(2)}{ma.group(3)}")
                ev = Event(
                    ma.group(1),
                    float(ma.group(2)),
                    "t" if ma.group(3) == "片" else ma.group(3),
                )
                events.append(ev)
            elif mb:
                # print(f"{dt} | {mb.group(2)} | {mb.group(1)}片")
                ev = Event(mb.group(2), float(mb.group(1)), "t")
                events.append(ev)
            else:
                # print(f"{dt} | [备注/未识别] {item}")
                nt = Notice(item)
                events.append(nt)
        action = Action(dt, events)
        actions.append(action)
    classification(actions)
    return actions


@dataclass
class RefValue:
    # half_life: (吸收半衰期_小时, 消除半衰期_小时)
    # dose: (常用单次剂量_mg, 相对基准的等效因数)
    half_life: Tuple[float, float]
    dose: Tuple[float, float]

    def strength(self, dose_mg: float, seconds: float) -> Tuple[float, float]:
        """
        根据给定的时间（秒）计算体内残余药量
        :param dose_mg: 服药剂量
        :param seconds: 服药后经过的秒数
        :return: (raw_value, scaled_value)
                 - raw_value: 体内当前残余的绝对剂量 (mg)
                 - scaled_value: 乘以等效因数后的归一化强度 (等效 mg)
        """
        if seconds <= 0:
            return (0.0, 0.0)
        t_h = seconds / 3600.0
        t_abs, t_elim = self.half_life
        base_mg, factor = self.dose
        k_a = math.log(2) / t_abs
        k_e = math.log(2) / t_elim
        if abs(k_a - k_e) < 1e-6:
            raw = dose_mg * k_a * t_h * math.exp(-k_a * t_h)
        else:
            raw = (
                dose_mg
                * (k_a / (k_a - k_e))
                * (math.exp(-k_e * t_h) - math.exp(-k_a * t_h))
            )
        scaled = (raw / base_mg) * factor
        return (raw, scaled)


def dtrange(start: datetime, end: datetime, step=timedelta(minutes=30), inclusive=True):
    current = start
    while current <= end if inclusive else current < end:
        yield current
        current += step


# 计算 [Min, Q1, Median, Q3, Max] 的辅助函数
def process_boxplot(values: List[float]) -> List[float]:
    if not values:
        return [0.0, 0.0, 0.0, 0.0, 0.0]
    arr = np.array(values)
    return [
        float(np.min(arr)),
        float(np.percentile(arr, 25)),
        float(np.median(arr)),
        float(np.percentile(arr, 75)),
        float(np.max(arr)),
    ]


def actions_to_dose_daily_datapoints_bzds(actions: List[Action]) -> dict:
    base = {
        "series": [
            {
                "name": "boxplot",
                "type": "boxplot",
                "data": [],
            }
        ]
    }
    mapping = {
        "阿普唑仑": 0,
        "艾司唑仑": 1,
        "劳拉西泮": 2,
        "氯硝西泮": 3,
        "地达西尼": 4,
    }
    meds = {
        # "地西泮": RefValue((20, 100), (10, 1)),  # 1x
        "阿普唑仑": RefValue((0.3, 12.0), (0.4, 2.0)),
        "艾司唑仑": RefValue((0.5, 17.0), (1.0, 1.0)),
        "劳拉西泮": RefValue((0.5, 12.0), (1.0, 1.0)),
        "氯硝西泮": RefValue((0.5, 30.0), (0.5, 2.0)),
        "地达西尼": RefValue((0.3, 4.5), (2.5, 0.4)),
    }
    med_records: Dict[str, List[Tuple[float, RefValue, datetime]]] = {}
    forward_dt = timedelta(days=3)
    step_dt = timedelta(minutes=5)
    segments: Dict[str, List[Tuple[datetime, datetime]]] = {}
    for ac in actions:
        dt = ac.dt
        for ev in ac.events:
            if type(ev) is not Event:
                continue
            q = ev.get_quantity("mg")
            if q is None:
                continue
            for name, value in meds.items():
                if ev.name.startswith(name):
                    if med_records.get(name):
                        med_records[name].append((q, value, dt))
                    else:
                        med_records[name] = [(q, value, dt)]
            pass
    # print(med_records)
    for name, records in med_records.items():
        if not records:
            segments[name] = []
            continue
        raw_intervals = [(rec[2], rec[2] + forward_dt) for rec in records]
        raw_intervals.sort(key=lambda x: x[0])
        merged_intervals = []
        for start, stop in raw_intervals:
            if not merged_intervals:
                merged_intervals.append((start, stop))
            else:
                prev_start, prev_stop = merged_intervals[-1]
                if start <= prev_stop:
                    merged_intervals[-1] = (prev_start, max(prev_stop, stop))
                else:
                    merged_intervals.append((start, stop))
        segments[name] = merged_intervals
    # print(segments)
    # dict {name, (point_ts, raw_strength, scaled_strength)}
    points: Dict[str, List[Tuple[datetime, float, float]]] = {}
    for name, segs in segments.items():
        buf: List[Tuple[datetime, float, float]] = []
        for tr in segs:
            start_dt, end_dt = tr
            recs = med_records[name]
            to_measure = list(filter(lambda x: start_dt <= x[2] <= end_dt, recs))
            for measure_dt in dtrange(*tr, step=step_dt):
                # measure_dt 是区间时间轴
                raw_strength, scaled_strength = (0.0, 0.0)
                for quantity, rv, start_tm in to_measure:
                    # seconds_past 是时间轴相对于 start_tm 的秒数
                    seconds_past = (measure_dt - start_tm).total_seconds()
                    s = rv.strength(quantity, seconds_past)
                    raw_strength += s[0]
                    scaled_strength += s[1]
                # print(
                #     f"{name} {start_dt.isoformat()} {measure_dt.isoformat()}:"
                #     f" raw={raw_strength} scaled={scaled_strength}"
                # )
                buf.append((measure_dt, raw_strength, scaled_strength))
        points[name] = buf
    points_peaks: Dict[str, List[Tuple[datetime, float, float]]] = {}
    for name, item_list in points.items():
        if not item_list:
            points_peaks[name] = []
            continue
        raw_strengths = np.array([item[1] for item in item_list])
        peak_indices, _ = find_peaks(raw_strengths, prominence=0.1, distance=5)
        points_peaks[name] = [item_list[i] for i in peak_indices]
    # for name, peaks in points_peaks.items():
    #     for p in peaks:
    #         print(f"{name} {p[0].isoformat()}: raw={p[1]} scaled={p[2]}")
    boxplot_zero = [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        ["-", "-", "-", "-", "-"],
    ]
    boxplot_data = [boxplot_zero] * len(mapping)
    for name, idx in mapping.items():
        items = points_peaks.get(name, [])
        if items:
            raw_vals = [item[1] for item in items]
            scaled_vals = [item[2] for item in items]
            raw_stats = [fmt_float(q) + "mg" for q in process_boxplot(raw_vals)]
            scaled_stats = process_boxplot(scaled_vals)
            boxplot_data[idx] = scaled_stats + [raw_stats]
        else:
            boxplot_data[idx] = boxplot_zero
    base["series"][0]["data"] = boxplot_data
    return base


def actions_to_sleep_datapoints(actions: List[Action]) -> dict:
    opacity = {"itemStyle": {"opacity": 0.5}}
    base = {
        "series": [
            {"name": "阿普唑仑", "type": "scatter", "data": []},  # 0
            {"name": "艾司唑仑", "type": "scatter", "data": []},  # 1
            {"name": "劳拉西泮", "type": "scatter", "data": []},  # 2
            {"name": "氯硝西泮", "type": "scatter", "data": []},  # 3
            {"name": "地达西尼", "type": "scatter", "data": []},  # 4
            {"name": "茶苯海明", "type": "scatter", "data": []},  # 5
            {"name": "莱博雷生", "type": "scatter", "data": []},  # 6
            {"name": "异丙嗪", "type": "scatter", "data": []},  # 7
            {"name": "喹硫平", "type": "scatter", "data": []},  # 8
            {"name": "曲唑酮", "type": "scatter", "data": []},  # 9
            {"name": "右佐匹克隆", "type": "scatter", "data": []},  # 10
            {"name": "佐匹克隆", "type": "scatter", "data": []},  # 11
            {"name": "唑吡坦", "type": "scatter", "data": []},  # 12
            {"name": "扎来普隆", "type": "scatter", "data": []},  # 13
            {"name": "米氮平", "type": "scatter", "data": []},  # 14
        ],
    }
    series_data_map = {i: {} for i in range(len(base["series"]))}
    for ac in actions:
        date_str = ac.dt.strftime("%Y-%m-%d %H:%M")
        midnight = ac.dt.replace(hour=0, minute=0, second=0, microsecond=0)
        time_sec = int((ac.dt - midnight).total_seconds())
        time_sec = time_sec - 86400 if ac.dt.time() >= time(12, 0, 0) else time_sec
        time_key = (date_str, time_sec)
        for ev in ac.events:
            if len(ev.applications) == 0 and ev.classification == Classification.Other:
                continue  # skip
            if type(ev) is not Event:
                continue
            q = ev.get_quantity("mg")
            if q is None:
                continue
            # info 字段
            info = ev.classification.value
            i = ",".join([j.value for j in ev.applications])
            info = f"{info}({i})" if len(i) > 0 else info
            # med 字段
            med = ""
            if type(ev) is Event:
                med = f"{ev.name} {ev.q()}"
            elif type(ev) is Notice:
                med = ev.msg
            # 匹配系列名
            for i, s in enumerate(base["series"]):
                name: str = s["name"]
                if name in ev.name:
                    if time_key not in series_data_map[i]:
                        series_data_map[i][time_key] = []
                    series_data_map[i][time_key].append([info, med])
                    break  # 有些药名字太像...
    for series_idx, point_dict in series_data_map.items():
        base["series"][series_idx]["data"] = [
            [dt, sec, items] for (dt, sec), items in point_dict.items()
        ]
    for b in base["series"]:
        b |= opacity
    # print(series_data_map)
    return base


def actions_to_datapoints(actions: List[Action]) -> dict:
    opacity = {"itemStyle": {"opacity": 0.5}}
    base = {
        "series": [
            {"name": "抗抑郁药", "type": "scatter", "data": []},  # 0
            {"name": "心境稳定剂", "type": "scatter", "data": []},  # 1
            {"name": "抗焦虑/镇静/安眠药", "type": "scatter", "data": []},  # 2
            {"name": "HRT类", "type": "scatter", "data": []},  # 3
            {"name": "补充剂", "type": "scatter", "data": []},  # 4
            {"name": "其他", "type": "scatter", "data": []},  # 5
        ],
    }
    # series_data_map[series_idx][(date_str, time_sec)] = [[info, med], ...]
    series_data_map = {i: {} for i in range(len(base["series"]))}
    for ac in actions:
        date_str = ac.dt.strftime("%Y-%m-%d %H:%M")
        midnight = ac.dt.replace(hour=0, minute=0, second=0, microsecond=0)
        time_sec = int((ac.dt - midnight).total_seconds())
        for ev in ac.events:
            if len(ev.applications) == 0 and ev.classification == Classification.Other:
                continue  # skip
            # info 字段
            info = ev.classification.value
            i = ",".join([j.value for j in ev.applications])
            info = f"{info}({i})" if len(i) > 0 else info
            # med 字段
            med = ""
            if type(ev) is Event:
                med = f"{ev.name} {ev.q()}"
            elif type(ev) is Notice:
                med = ev.msg
            # 分类判断
            apps = set(ev.applications)
            c = ev.classification
            if Application.Antidepressants in apps or (
                c
                in {
                    Classification.SSRIs,
                    Classification.SNRIs,
                    Classification.SARIs,
                    Classification.NDRIs,
                    Classification.NaSSAs,
                }
                and Application.Hypnotic not in apps
            ):
                series_idx = 0
            elif c == Classification.MoodStabilizer:
                series_idx = 1
            elif (
                c in {Classification.BZDs, Classification.ZDurgs, Classification.ORAs}
                or Application.Hypnotic in apps
                or Application.Sedative in apps
                or Application.Anxiolytics in apps
            ):
                series_idx = 2
            elif (
                c == Classification.HRT
                or Application.Estrogen in apps
                or Application.Antiandrogen in apps
            ):
                series_idx = 3
            elif c == Classification.Supplements:
                series_idx = 4
            else:
                series_idx = 5
            time_key = (date_str, time_sec)
            if time_key not in series_data_map[series_idx]:
                series_data_map[series_idx][time_key] = []
            series_data_map[series_idx][time_key].append([info, med])
    for series_idx, point_dict in series_data_map.items():
        base["series"][series_idx]["data"] = [
            [dt, sec, items] for (dt, sec), items in point_dict.items()
        ]
    for b in base["series"]:
        b |= opacity
    return base


def main():
    data_med: List[Action] = []
    data_hrt: List[Action] = []
    with open(TEMPDATA / "吃药.md", "r") as f:
        data_med = preprocess(f)
    with open(TEMPDATA / "hrt.md", "r") as f:
        data_hrt = preprocess(f)
    actions = data_med + data_hrt
    # for ac in actions:
    #     if ac.dt == datetime.fromisoformat("2025-12-28T22:12:00.000000+08:00"):
    #         print(ac)
    # print(ac)
    with open(CHARTS / "the-art-of-medication-schedule-data-1.json", "w") as f:
        dp = actions_to_datapoints(actions)
        json.dump(dp, f)
    with open(CHARTS / "the-art-of-medication-schedule-data-2.json", "w") as f:
        dp = actions_to_dose_daily_datapoints_bzds(actions)
        json.dump(dp, f)
    with open(CHARTS / "the-art-of-medication-schedule-data-4.json", "w") as f:
        dp = actions_to_sleep_datapoints(actions)
        json.dump(dp, f)
    pass


if __name__ == "__main__":
    main()
