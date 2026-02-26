# 命令行调用模板

## 基本调用格式

```bash
# 调用架构师
openclaw agent --agent architect --message "<提示词>" --timeout 300

# 调用软件工程师
openclaw agent --agent software-engineer --message "<提示词>" --timeout 600

# 调用测试工程师
openclaw agent --agent tester --message "<提示词>" --timeout 300

# 调用产品经理
openclaw agent --agent product-manager --message "<提示词>" --timeout 300

# 调用交互设计师
openclaw agent --agent ui-designer --message "<提示词>" --timeout 300
```

## 带上下文的调用

```bash
# 传入项目路径
openclaw agent --agent software-engineer \
  --message "在 ~/Projects/myapp 中实现用户登录功能" \
  --timeout 600

# 传入详细需求
openclaw agent --agent product-manager \
  --message "分析需求：在播客应用中实现定时提醒功能" \
  --timeout 300
```

## 输出处理

```bash
# 获取输出
result=$(openclaw agent --agent architect --message "设计架构" --timeout 300)

# 解析JSON（如果使用--json）
openclaw agent --agent architect --message "设计架构" --json
```

## 常用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --agent | Agent ID | main |
| --message | 提示词 | - |
| --timeout | 超时秒数 | 600 |
| --thinking | 思考级别 | off |
| --json | JSON输出 | false |
