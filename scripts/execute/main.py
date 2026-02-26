#!/usr/bin/env python3
"""
执行脚本 - 调用软件工程师和交互设计师Agent
"""

import argparse
import subprocess
import sys


def call_agent(agent_id: str, prompt: str, timeout: int = 600) -> str:
    """调用OpenClaw Agent"""
    cmd = ["openclaw", "agent", "--agent", agent_id, "--message", prompt, "--timeout", str(timeout)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 30)
    return result.stdout if result.returncode == 0 else result.stderr


def main():
    parser = argparse.ArgumentParser(description="代码执行 - 软件工程师 + 交互设计师")
    parser.add_argument("--project", required=True, help="项目名称")
    parser.add_argument("--project-path", help="项目路径")
    parser.add_argument("--task", required=True, help="任务描述")
    parser.add_argument("--skip-ui", action="store_true", help="跳过UI设计")
    args = parser.parse_args()
    
    project_path = args.project_path or f"~/Projects/{args.project}"
    
    if not args.skip_ui:
        print(f"\n🎨 阶段1: 交互设计师UI设计")
        print("=" * 50)
        
        ui_prompt = f"""你是交互设计师。请设计以下功能的界面：

项目：{args.project}
项目路径：{project_path}

任务：{args.task}

请输出：
1. 页面布局（文字描述）
2. 交互流程
3. 组件建议
4. 用户体验要点

请用中文回复。"""
        
        ui_result = call_agent("ui-designer", ui_prompt)
        print(ui_result)
    
    print(f"\n🧑‍💻 阶段2: 软件工程师代码实现")
    print("=" * 50)
    
    code_prompt = f"""你是软件工程师。请实现以下功能：

项目：{args.project}
项目路径：{project_path}

任务：{args.task}

请：
1. 先了解项目结构
2. 编写实现代码
3. 确保代码规范

请用中文回复，给出完整代码。"""
    
    code_result = call_agent("software-engineer", code_prompt, timeout=900)
    print(code_result)
    
    print(f"\n✅ 执行完成！")


if __name__ == "__main__":
    main()
