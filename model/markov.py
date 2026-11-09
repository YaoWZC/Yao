#!/usr/bin/env python3
"""三状态 Markov 队列模型骨架（健康 S / 进展 P / 死亡 D）。

读取 model/params.csv -> 计算两种策略的总成本与 QALY -> 写 outputs/base_case.md。

⚠️ 参数为 PLACEHOLDER，本脚本只验证"管道能跑通"，结果不得用于任何真实决策。
仅用 Python 标准库，无需安装依赖。
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARAMS = ROOT / "model" / "params.csv"
OUTPUT = ROOT / "outputs" / "base_case.md"


def load_params(path):
    """把 params.csv 读成 {key: float}，同时保留原始行用于报告。"""
    if not path.exists():
        sys.exit(f"找不到参数表: {path}")
    values, rows = {}, []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
            try:
                values[row["key"]] = float(row["value"])
            except (TypeError, ValueError):
                sys.exit(f"参数 {row['key']} 的 value 不是数字: {row['value']!r}")
    return values, rows


def run(p, drug_cost):
    """跑一条策略，返回 (总成本, 总QALY)。"""
    r = p["discount_rate"]
    cycle = p["cycle_years"]
    s, prog = 1.0, 0.0
    total_cost = total_qaly = 0.0

    for t in range(int(p["n_cycles"])):
        discount = 1.0 / (1.0 + r) ** (t * cycle)
        total_cost += (s * p["cost_s"] + prog * p["cost_p"] + s * drug_cost) * discount
        total_qaly += (s * p["util_s"] + prog * p["util_p"]) * cycle * discount

        s_next = s * (1.0 - p["p_sp_std"] - p["p_spd"])
        prog_next = prog * (1.0 - p["p_pd"]) + s * p["p_sp_std"]
        s, prog = s_next, prog_next

    return total_cost, total_qaly


def main():
    p, rows = load_params(PARAMS)

    # 干预策略只改 健康→进展 概率与药品成本
    std_cost, std_qaly = run(p, 0.0)
    p_new = dict(p, p_sp_std=p["p_sp_new"])
    new_cost, new_qaly = run(p_new, p["drug_cost_new"])

    d_cost = new_cost - std_cost
    d_qaly = new_qaly - std_qaly
    icer = d_cost / d_qaly if d_qaly else float("inf")
    threshold = p["threshold"]
    verdict = "具有成本效果" if icer <= threshold else "不具有成本效果"

    lines = [
        "# Base case 结果",
        "",
        "> 自动生成，请勿手工编辑。参数为占位符时结论无效。",
        "",
        "| 指标 | 对照策略 | 干预策略 |",
        "| --- | --- | --- |",
        f"| 总成本 | {std_cost:,.0f} | {new_cost:,.0f} |",
        f"| 总 QALY | {std_qaly:,.3f} | {new_qaly:,.3f} |",
        "",
        f"- 增量成本：**{d_cost:,.0f}**",
        f"- 增量 QALY：**{d_qaly:,.4f}**",
        f"- ICER：**{icer:,.0f}** 元/QALY",
        f"- 阈值：{threshold:,.0f} 元/QALY → {verdict}",
        "",
        "## 参数快照",
        "",
        "| key | value | 来源 |",
        "| --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row['key']} | {row['value']} | {row['source']} |")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"已写入 {OUTPUT}")
    print(f"ICER = {icer:,.0f} 元/QALY（{verdict}）")


if __name__ == "__main__":
    main()
