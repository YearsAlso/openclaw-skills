---
name: multi-agent-planner
description: |
  多Agent计划阶段。使用产品经理和架构师分析需求，设计架构。
  Activate when user wants to plan a development task.
---

# 多Agent计划阶段

## 用途
分析需求、设计架构，为开发做准备。

## 使用方式

```bash
python3 ~/.openclaw/workspace/multi_agent_dev.py --project <项目名> analyze --requirement "<需求描述>"
python3 ~/.openclaw/workspace/multi_agent_dev.py --project <项目名> architect --task "<架构任务>"
```

## Agent角色
- 📋 product-manager: 需求分析
- 👨‍💻 architect: 架构设计

## 输出
- 需求分析报告
- 架构设计方案
