# 外部来源登记

凡不是来自 `evidence/extraction.csv` 的参数来源，必须在此登记，`checks/verify_params.py` 才会认可。

每行一个来源，写法是「来源名称」+ 空格 + 破折号（U+2014）+ 空格 + 说明/链接。

示例（代码块内的内容不会被解析，可以直接照抄格式）：

```
WHO-CHOICE 2023 — 单位成本上限，https://www.who.int/choice
中国卫生统计年鉴 2023 — 人均医疗支出
```
