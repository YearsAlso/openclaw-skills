#!/usr/bin/env python3
"""
审查脚本 - 调用测试工程师和软件工程师Agent
"""

import argparse
import subprocess
import sys


def call_agent(agent_id: str, prompt: str, timeout: int = 300) -> str:
    """调用OpenClaw Agent"""
    cmd = ["openclaw", "agent", "--agent", agent_id, "--message", prompt, "--timeout", str(timeout)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 30)
    return result.stdout if result.returncode == 0 else result.stderr


def main():
    parser = argparse.ArgumentParser(description="代码审查 - 测试工程师 + 软件工程师")
    parser.add_argument("--project", required=True, help="项目名称")
    parser.add_argument("--project-path", help="项目路径")
    parser.add_argument("--task", required=True, help="任务描述")
    parser.add_argument("--code", help="代码内容（可选）")
    args = parser.parse_args()
    
    project_path = args.project_path or f"~/Projects/{args.project}"
    
    print(f"\n🧪 阶段1: 测试工程师编写测试用例")
    print("=" * 50)
    
    test_prompt = f"""你是测试工程师。请编写以下功能的测试用例：

项目：{args.project}
项目路径：{project_path}

任务：{args.task}

请输出：
1. 测试用例列表（5-10个）
2. 每个用例的步骤和预期结果
3. 边界条件
4. 异常情况

请用中文回复。"""
    
    test_result = call_agent("tester", test_prompt)
    print(test_result)
    
    print(f"\n🧑‍💻 阶段2: 软件工程师代码审查")
    print("=" * 50)
    
    review_prompt = f"""你是软件工程师。请审查以下代码：

项目：{args.project}
项目路径：{project_path}

任务：{args.task}

请输出：
1. 代码问题
2. 改进建议
3. 安全问题（如有）
4. 性能建议（如有）

请用中文回复。"""
    
    review_result = call_agent("software-engineer", review_prompt)
    print(review_result)
    
    print(f"\n✅ 审查完成！")


if __name__ == "__main__":
    main()
