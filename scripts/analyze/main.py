#!/usr/bin/env python3
"""
需求分析脚本 - 调用产品经理和架构师Agent
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
    parser = argparse.ArgumentParser(description="需求分析 - 产品经理 + 架构师")
    parser.add_argument("--project", required=True, help="项目名称")
    parser.add_argument("--project-path", help="项目路径")
    parser.add_argument("--requirement", required=True, help="需求描述")
    args = parser.parse_args()
    
    project_path = args.project_path or f"~/Projects/{args.project}"
    
    print(f"\n📋 阶段1: 产品经理需求分析")
    print("=" * 50)
    
    # 产品经理分析需求
    pm_prompt = f"""你是产品经理。请分析以下需求：

项目：{args.project}
项目路径：{project_path}

需求：{args.requirement}

请输出：
1. 需求概述
2. 用户故事（3-5条）
3. 功能列表（按优先级排序）
4. 核心业务流程
5. 边界情况

请用中文回复。"""
    
    pm_result = call_agent("product-manager", pm_prompt)
    print(pm_result)
    
    print(f"\n👨‍💻 阶段2: 架构师架构设计")
    print("=" * 50)
    
    # 架构师设计架构
    arch_prompt = f"""你是架构师。请设计以下需求的架构：

项目：{args.project}
项目路径：{project_path}

需求：{args.requirement}

请输出：
1. 技术选型建议
2. 模块划分
3. 数据库设计（如适用）
4. API设计（如适用）
5. 架构图（Mermaid格式）

请用中文回复。"""
    
    arch_result = call_agent("architect", arch_prompt)
    print(arch_result)
    
    print(f"\n✅ 需求分析完成！")


if __name__ == "__main__":
    main()
