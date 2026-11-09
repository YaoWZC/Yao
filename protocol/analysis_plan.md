# 分析计划

> 状态：**模板**。本文件定义"什么算跑对了"，agent 按此执行。

## 主分析（base case）

1. 读取 `model/params.csv` 的 `value` 列
2. 运行 `python3 model/markov.py`
3. 输出写入 `outputs/base_case.md`，须包含：
   - 每策略的总成本、总 QALY
   - 增量成本、增量 QALY
   - **ICER**（增量成本 / 增量 QALY）
   - 与阈值的比较结论

## 敏感性分析

| 类型 | 做法 | 输出 |
|---|---|---|
| 单因素（DSA） | 每次一个参数取 `low` / `high`，其余不变 | `outputs/dsa.csv` |
| 概率（PSA） | 按分布抽样 N 次（TODO: N=1000） | `outputs/psa.csv` + CE 平面图 |

## 验收标准

- [ ] `python3 checks/verify_params.py` 通过（每个参数的 source 都可追溯）
- [ ] base case 可重复：同一份 `params.csv` 两次运行结果一致
- [ ] 结果表中的每个数字都能在 `outputs/base_case.md` 找到
- [ ] 参数改动只发生在 `params.csv`，代码里无硬编码数值

## 报告口径

- ICER 单位：元 / QALY
- 低于阈值 → 判定为"具有成本效果"
- 阈值来源必须写明，不得使用未注明出处的经验值

## 不做的事

- 不替研究者决定模型结构（Markov vs 决策树 vs 离散事件）
- 不对缺失参数做插补
- 不在未跑通 base case 的情况下报告敏感性分析结果
