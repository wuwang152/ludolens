# LudoLens (MVP v1)

LudoLens 是一个面向普通玩家、家长和研究者的开源工具，用来分析游戏的商业化机制、消费压力、时间负担和潜在不透明设计。

> 当前版本是本地原型：使用样本 CSV 数据 + Streamlit 可视化，不依赖爬虫、数据库或外部 API。

## 功能概览
- 读取本地样本数据：`data/sample_games.csv`
- 数据校验（字段完整性、数值范围、唯一性）
- 计算五个输出字段：
  - `consumption_pressure_score`
  - `time_burden_score`
  - `transparency_risk_score`
  - `total_risk_score`
  - `risk_level`
- Streamlit 页面支持：
  - 基础信息表
  - 按平台/类型/商业模式筛选
  - 风险分图表（Altair）
  - 单款游戏分析卡片
- pytest 基础测试

## 项目结构

```text
ludolens/
├── AGENTS.md
├── README.md
├── requirements.txt
├── app.py
├── data/
│   └── sample_games.csv
├── docs/
│   ├── methodology.md
│   └── project_idea.md
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── schema.py
│   └── scoring.py
└── tests/
    └── test_scoring.py
```

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

运行应用：

```bash
streamlit run app.py
```

运行测试：

```bash
pytest -q
```

## 方法说明
- 项目定位与边界：`docs/project_idea.md`
- 评分方法与局限：`docs/methodology.md`

## 声明
本项目分数为启发式风险信号，不构成对游戏质量、合规性或经营行为的最终判断。
