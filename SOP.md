# SOP — 本仓库的工作规矩

## 1. 引用与出处

- 任何进入 `model/params.csv` 的数值，`source` 列必须是：
  - `evidence/extraction.csv` 中某行的 `literature_id`，或
  - 一个可公开访问的来源（写全称，如 `WHO-CHOICE 2023`）。
- 任何进入 `manuscript/` 的引用，必须带 DOI 或 PMID。
- **禁止**凭记忆填写页码、表号、DOI。查不到就写 `NA` 并在 `note` 说明。
- 校验脚本：`python3 checks/verify_params.py` 必须通过。

## 2. 数值

- 参数值只能来自 `model/params.csv`，**不得在代码里硬编码**。
- 改参数 = 改 CSV；改模型 = 改代码。两者不混。
- 每个结果数字都要能追到 `outputs/base_case.md` 的某一行。

## 3. 数据合规

- 本仓库**不存放**患者级数据（姓名、病历号、处方明细、检验值明细）。
- 需要真实数据时，只用聚合后的统计量，且经伦理与脱敏审核。
- 模型输入以文献值和敏感性范围为主。

## 4. 变更流程

- 所有改动走分支 + PR，分支前缀 `agent/`（agent）或 `feat/`（人）。
- PR 必须说明：改了什么、为什么、如何验证。
- 涉及 `model/` 的 PR，必须附 base case 的运行结果。

## 5. 报告口径

- 成本用当地货币单位，注明年份与价格水平。
- 效果用 QALY，注明效用值来源与测量工具。
- ICER 必须与阈值一起报告；阈值来源写进 `protocol/analysis_plan.md`。
