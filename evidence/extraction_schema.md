# 数据提取表字段定义

`extraction.csv` 每行一条研究或一个数据来源。**先定义，再填**——未在此定义的列不得出现在 CSV 里。

| 列 | 含义 | 取值约束 |
|---|---|---|
| `literature_id` | 文献唯一标识 | `作者年份` 或 DOI，全表唯一 |
| `citation` | 完整引文 | 必须有标题与期刊 |
| `doi` | DOI | 无则 `NA` |
| `country` | 研究所在国家/地区 | — |
| `population` | 人群描述 | — |
| `intervention` | 干预 | — |
| `comparator` | 对照 | — |
| `perspective` | 视角 | 卫生体系 / 全社会 / 支付方 |
| `time_horizon` | 时间跨度 | 如 `10 years`、`lifetime` |
| `discount_rate` | 贴现率 | 0–1 小数，如 `0.05` |
| `currency` | 货币 | ISO 代码，如 `CNY` |
| `price_year` | 价格年份 | 4 位年份 |
| `cost_per_qaly` | 报告的 ICER | 数值或 `NA` |
| `page_or_table` | 该数据的出处位置 | 页码或表号，**必填** |
| `note` | 备注 | 提取者判断、歧义说明 |

## 提取规则

1. 一个字段一个来源；同一行的多个数值若来自不同表，拆成多行。
2. 原文没有的数值写 `NA`，**不要估算、不要插补**。
3. 单位不一致时，在 `note` 写明换算方式，换算后保留原值。
4. 只读英文/中文全文；只有摘要的不提取结果数值。
