# OpenClaw Multi-Agent Skills

多Agent协同开发技能库，基于OpenClaw框架。

## 目录结构

```
openclaw-skills/
├── README.md                        # 项目说明
├── scripts/                         # 脚本目录
│   ├── analyze/                   # 需求分析脚本
│   │   └── main.py              # 产品经理 + 架构师
│   ├── execute/                  # 代码执行脚本
│   │   └── main.py              # 软件工程师 + 交互设计师
│   ├── review/                   # 代码审查脚本
│   │   └── main.py              # 测试工程师 + 软件工程师
│   └── coordinator/               # 协调器脚本
│       └── main.py              # 完整流程
├── multi-agent-planner/          # Skill: 计划阶段
├── multi-agent-executor/         # Skill: 执行阶段
├── multi-agent-reviewer/         # Skill: 审查阶段
├── multi-agent-coordinator/     # Skill: 调度器
└── references/                  # 参考资料
    ├── agent_roles.md           # Agent角色定义
    ├── cli_templates.md        # 命令行模板
    ├── prompt_templates.md    # 提示词模板
    └── workflows.md           # 工作流图
```

## 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/YearsAlso/openclaw-skills.git
cd openclaw-skills
```

### 2. 配置Agent
```bash
# 添加需要的Agent
openclaw agents add product-manager --workspace ~/.openclaw/agents/product-manager/agent
openclaw agents add architect --workspace ~/.openclaw/agents/architect/agent
openclaw agents add software-engineer --workspace ~/.openclaw/agents/software-engineer/agent
openclaw agents add tester --workspace ~/.openclaw/agents/tester/agent
openclaw agents add ui-designer --workspace ~/.openclaw/agents/ui-designer/agent
```

## 使用方式

### 需求分析（产品经理 + 架构师）
```bash
python3 scripts/analyze/main.py --project myapp --requirement "实现用户登录功能"
```

### 代码执行（软件工程师 + 交互设计师）
```bash
python3 scripts/execute/main.py --project myapp --task "实现登录API"
```

### 代码审查（测试工程师 + 软件工程师）
```bash
python3 scripts/review/main.py --project myapp --task "审查登录模块"
```

### 完整流程（协调器）
```bash
python3 scripts/coordinator/main.py --project myapp --requirement "实现用户系统"
```

### 可选参数
```bash
# 跳过UI设计
python3 scripts/coordinator/main.py --project myapp --requirement "xxx" --skip-ui

# 跳过测试
python3 scripts/coordinator/main.py --project myapp --requirement "xxx" --skip-test
```

## Agent角色

| Agent | 职责 |
|-------|------|
| product-manager | 需求分析、产品设计 |
| architect | 架构设计、技术选型 |
| software-engineer | 代码实现、代码审查 |
| tester | 测试用例、质量保证 |
| ui-designer | 界面设计、交互流程 |

## 参考资料

- `references/agent_roles.md` - Agent角色定义
- `references/prompt_templates.md` - 提示词模板
- `references/workflows.md` - 工作流图

## 许可证

MIT
