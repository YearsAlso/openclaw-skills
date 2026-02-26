#!/usr/bin/env python3
"""
协调器脚本 - 协调完整开发流程
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
    parser = argparse.ArgumentParser(description="开发流程协调器")
    parser.add_argument("--project", required=True, help="项目名称")
    parser.add_argument("--project-path", help="项目路径")
    parser.add_argument("--requirement", required=True, help="需求描述")
    parser.add_argument("--skip-ui", action="store_true", help="跳过UI设计")
    parser.add_argument("--skip-test", action="store_true", help="跳过测试")
    args = parser.parse_args()
    
    project_path = args.project_path or f"~/Projects/{args.project}"
    
    print(f"\n{'='*60}")
    print(f"🚀 完整开发流程启动")
    print(f"{'='*60}")
    print(f"项目：{args.project}")
    print(f"需求：{args.requirement}")
    print(f"{'='*60}\n")
    
    # 阶段1: 需求分析
    print(f"\n📋 阶段1: 产品经理需求分析")
    print("=" * 50)
    
    pm_prompt = f"""你是产品经理。请分析以下需求：

项目：{args.project}
需求：{args.requirement}

请输出：
1. 需求概述
2. 用户故事（3-5条）
3. 功能列表（按优先级）
4. 业务流程

请用中文回复。"""
    
    print(call_agent("product-manager", pm_prompt))
    
    # 阶段2
    print(f: 架构设计"\n👨‍💻 阶段2: 架构师架构设计")
    print("=" * 50)
    
    arch_prompt = f"""你是架构师。请设计以下需求的架构：

项目：{args.project}
需求：{args.requirement}

请输出：
1. 技术选型
2. 模块划分
3. 数据库设计（如适用）
4. 架构图（Mermaid）

请用中文回复。"""
    
    print(call_agent("architect", arch_prompt))
    
    # 阶段3: UI设计（可选）
    if not args.skip_ui:
        print(f"\n🎨 阶段3: 交互设计师UI设计")
        print("=" * 50)
        
        ui_prompt = f"""你是交互设计师。请设计以下功能的界面：

项目：{args.project}
任务：{args.requirement}

请输出：
1. 页面布局
2. 交互流程
3. 组件建议

请用中文回复。"""
        
        print(call_agent("ui-designer", ui_prompt))
    
    # 阶段4: 代码实现
    print(f"\n🧑‍💻 阶段4: 软件工程师代码实现")
    print("=" * 50)
    
    code_prompt = f"""你是软件工程师。请实现以下功能：

项目：{args.project}
任务：{args.requirement}

请：
1. 了解项目结构
2. 编写实现代码
3. 确保代码规范

请用中文回复，给出完整代码。"""
    
    print(call_agent("software-engineer", code_prompt, timeout=900))
    
    # 阶段5: 测试审查（可选）
    if not args.skip_test:
        print(f"\n🧪 阶段5: 测试工程师编写测试用例")
        print("=" * 50)
        
        test_prompt = f"""你是测试工程师。请编写以下功能的测试用例：

项目：{args.project}
任务：{args.requirement}

请输出测试用例列表和步骤。"""
        
        print(call_agent("tester", test_prompt))
    
    print(f"\n{'='*60}")
    print(f"✅ 完整开发流程完成！")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
