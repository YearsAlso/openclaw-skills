---
name: multi-agent-reviewer
description: |
  多Agent审查阶段。使用测试工程师编写测试用例，审查代码质量。
  Activate when user wants to review code or write tests.
---

# 多Agent审查阶段

## 用途
编写测试用例、审查代码质量。

## 使用方式

```bash
# 测试用例
python3 ~/.openclaw/workspace/multi_agent_dev.py --project <项目名> test --task "<测试任务>"

# 代码审查（使用软件工程师）
python3 ~/.openclaw/workspace/multi_agent_dev.py --project <项目名> code --task "审查代码质量"
```

## Agent角色
- 🧪 tester: 测试用例
- 🧑‍💻 software-engineer: 代码审查

## 输出
- 测试用例
- 代码审查报告
