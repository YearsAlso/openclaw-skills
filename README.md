# OpenClaw Multi-Agent Skills

多Agent协同开发技能库，基于OpenClaw框架。

## 目录结构

```
openclaw-skills/
├── multi_agent_dev.py      # 多Agent协同开发脚本
├── multi-agent-planner/    # 计划阶段Skill
├── multi-agent-executor/   # 执行阶段Skill
├── multi-agent-reviewer/   # 审查阶段Skill
└── multi-agent-coordinator/ # 核心调度器Skill
```

## Skills说明

### 1. multi-agent-planner (计划阶段)
- 📋 product-manager: 需求分析
- 👨‍💻 architect: 架构设计

### 2. multi-agent-executor (执行阶段)
- 🧑‍💻 software-engineer: 代码实现
- 🎨 ui-designer: 界面设计

### 3. multi-agent-reviewer (审查阶段)
- 🧪 tester: 测试用例
- 🧑‍💻 software-engineer: 代码审查

### 4. multi-agent-coordinator (核心调度器)
协调完整开发流程

## 使用方式

```bash
# 需求分析
python3 multi_agent_dev.py --project <项目名> analyze --requirement "<需求>"

# 架构设计
python3 multi_agent_dev.py --project <项目名> architect --task "<任务>"

# 代码实现
python3 multi_agent_dev.py --project <项目名> code --task "<任务>"

# 测试用例
python3 multi_agent_dev.py --project <项目名> test --task "<任务>"

# UI设计
python3 multi_agent_dev.py --project <项目名> design --task "<任务>"

# 完整工作流
python3 multi_agent_dev.py --project <项目名> run --requirement "<需求>"
```

## 配置Agent

需要先配置以下Agent：

```bash
openclaw agents add product-manager --workspace ~/.openclaw/agents/product-manager/agent
openclaw agents add architect --workspace ~/.openclaw/agents/architect/agent
openclaw agents add software-engineer --workspace ~/.openclaw/agents/software-engineer/agent
openclaw agents add tester --workspace ~/.openclaw/agents/tester/agent
openclaw agents add ui-designer --workspace ~/.openclaw/agents/ui-designer/agent
```

## 许可证

MIT
