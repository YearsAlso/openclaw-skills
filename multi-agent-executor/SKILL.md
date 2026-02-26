---
name: multi-agent-executor
description: |
  多Agent执行阶段。使用软件工程师实现代码，使用交互设计师设计界面。
  Activate when user wants to implement code or design UI.
---

# 多Agent执行阶段

## 用途
实现代码、设计UI，完成具体开发任务。

## 使用方式

```bash
# 代码实现
python3 ~/.openclaw/workspace/multi_agent_dev.py --project <项目名> code --task "<开发任务>"

# UI设计
python3 ~/.openclaw/workspace/multi_agent_dev.py --project <项目名> design --task "<设计任务>"
```

## Agent角色
- 🧑‍💻 software-engineer: 代码实现
- 🎨 ui-designer: 界面设计

## 输出
- 实现代码
- UI设计方案
