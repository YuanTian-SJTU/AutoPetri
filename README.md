# Petri网可视化与分析工具

## 项目简介
本项目支持将仓库/物流网络的 Excel 数据一键转换为 Petri 网（PNML），并可在网页中交互式可视化。

## 使用流程
1. **准备数据**：编辑 `input.xlsx`，包含节点、连边、需求等信息。
2. **生成PNML**：运行 `xlsx_to_pnml_woped.py`，自动生成 Woped 兼容的 `input_woped.pnml`。
3. **网页可视化**：用浏览器打开 `petri_net_visualization.html`，选择 `input_woped.pnml` 文件，即可交互式浏览和分析网络结构。

## 主要文件说明
- `input.xlsx`：输入数据（节点、连边、需求），可用Excel编辑。
- `xlsx_to_pnml_woped.py`：将Excel数据转为标准Petri网PNML文件，支持Woped和网页可视化。
- `input_woped.pnml`：自动生成的Petri网模型文件。
- `petri_net_visualization.html`：网页可视化工具，支持节点属性悬浮提示。

## 快速开始
1. 安装依赖：`pip install pandas openpyxl`
2. 编辑/准备好 `input.xlsx`
3. 运行：
   ```bash
   python xlsx_to_pnml_woped.py
   ```
4. 用浏览器打开 `petri_net_visualization.html`，选择生成的 `input_woped.pnml` 文件即可。

## 特色功能
- 节点属性（如经纬度、存储量）自动写入PNML并可网页悬浮查看
- 支持标准Petri网分析工具（如Woped）
- 网页端交互式可视化，无需后端

---
如需定制或扩展，欢迎联系开发者。