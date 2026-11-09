#!/usr/bin/env python3
"""校验 model/params.csv 的可追溯性与取值范围。

检查三件事：
1. 每个参数的 source 能解析——要么是 evidence/extraction.csv 里的 literature_id，
   要么是 evidence/external_sources.md 里登记过的外部来源。
2. low <= value <= high（若提供了上下限）。
3. 必需键齐全。

退出码：0 = 全部通过；1 = 有问题（会逐条列出）。
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARAMS = ROOT / "model" / "params.csv"
EXTRACTION = ROOT / "evidence" / "extraction.csv"
EXTERNAL = ROOT / "evidence" / "external_sources.md"

REQUIRED = [
    "cycle_years", "n_cycles", "discount_rate",
    "p_spd", "p_pd", "p_sp_std", "p_sp_new",
    "cost_s", "cost_p", "drug_cost_new",
    "util_s", "util_p", "threshold",
]


def known_sources():
    ids = set()
    if EXTRACTION.exists():
        with EXTRACTION.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("literature_id"):
                    ids.add(row["literature_id"].strip())
    if EXTERNAL.exists():
        in_fence = False
        for line in EXTERNAL.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            # 只认「来源名称 — 说明」格式，且不在示例代码块内
            if in_fence or not line or line.startswith("#") or " — " not in line:
                continue
            ids.add(line.split(" — ", 1)[0].strip())
    return ids


def main():
    problems = []
    rows = []
    if not PARAMS.exists():
        sys.exit(f"找不到 {PARAMS}")
    with PARAMS.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    keys = {r["key"] for r in rows}
    for k in REQUIRED:
        if k not in keys:
            problems.append(f"缺少必需参数: {k}")

    sources = {r["source"].strip() for r in rows if r.get("source")}
    placeholders = sum(1 for r in rows if r.get("source", "").strip() == "PLACEHOLDER")
    known = known_sources()
    unresolved = sorted(s for s in sources if s not in known and s != "PLACEHOLDER")

    for r in rows:
        key = r.get("key", "?")
        try:
            v = float(r["value"])
        except (TypeError, ValueError):
            problems.append(f"{key}: value 不是数字")
            continue
        for bound in ("low", "high"):
            raw = (r.get(bound) or "").strip()
            if raw:
                try:
                    b = float(raw)
                except ValueError:
                    problems.append(f"{key}: {bound} 不是数字")
                    continue
                if (bound == "low" and v < b) or (bound == "high" and v > b):
                    problems.append(f"{key}: value={v} 不在 {bound}={b} 的范围内")

    print(f"参数条数: {len(rows)}")
    print(f"已登记来源: {len(known)}")
    if placeholders:
        print(f"⚠️ 仍为 PLACEHOLDER 的参数: {placeholders} 条（填完 source 后本项消失）")
    if unresolved:
        print("❌ 无法解析的来源:")
        for s in unresolved:
            print(f"   - {s}")
    if problems:
        print("❌ 取值问题:")
        for p in problems:
            print(f"   - {p}")

    if placeholders or unresolved or problems:
        print("\n结果: 未通过（这是骨架阶段的预期状态）")
        return 1
    print("\n结果: 通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
