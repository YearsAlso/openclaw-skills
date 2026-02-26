#!/usr/bin/env python3
"""
多 Agent 协同开发脚本 (OpenClaw Agent 版)
=====================================

用途：
    多 Agent 协作进行软件开发，使用 OpenClaw 的真实 Agent。
    
功能：
    - 使用 OpenClaw 真实 Agent：产品经理、架构师、软件工程师、测试工程师、交互设计师
    - 支持任务分配和执行
    - 支持串行/并行执行模式
    
使用示例：
    # 分析需求
    python multi_agent_dev.py analyze --project castmind --requirement "实现用户登录功能"
    
    # 架构设计
    python multi_agent_dev.py architect --project castmind --task "设计登录模块架构"
    
    # 代码实现
    python multi_agent_dev.py code --project castmind --task "实现登录API"
    
    # 测试
    python multi_agent_dev.py test --project castmind --task "编写登录测试用例"
    
    # 设计
    python multi_agent_dev.py design --project castmind --task "设计登录页面UI"

配置：
    使用 OpenClaw 已配置的 Agent：
    - product-manager (产品经理)
    - architect (架构师)
    - software-engineer (软件工程师)
    - tester (测试工程师)
    - ui-designer (交互设计师)
"""

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

# ============ 枚举 ============
class AgentRole(Enum):
    """Agent角色"""
    COORDINATOR = "coordinator"          # 主 Agent：任务规划、分配
    PRODUCT_MANAGER = "product-manager"   # 产品经理
    ARCHITECT = "architect"               # 架构师
    SOFTWARE_ENGINEER = "software-engineer"  # 软件工程师
    TESTER = "tester"                    # 测试工程师
    UI_DESIGNER = "ui-designer"         # 交互设计师


# ============ Agent 映射 ============
AGENT_MAP = {
    "product-manager": "📋 产品经理",
    "architect": "👨‍💻 架构师",
    "software-engineer": "🧑‍💻 软件工程师",
    "tester": "🧪 测试工程师",
    "ui-designer": "🎨 交互设计师",
}


# ============ OpenClaw 调用 ============
class OpenClawAgent:
    """OpenClaw Agent 调用类"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.name = AGENT_MAP.get(agent_id, agent_id)
    
    def call(self, prompt: str, timeout: int = 300) -> str:
        """调用 OpenClaw Agent"""
        print(f"\n{'='*50}")
        print(f"🤖 调用 {self.name}...")
        print(f"{'='*50}")
        
        # 构建命令 - 使用 openclaw agent 命令，指定 agent id
        cmd = [
            "openclaw", "agent",
            "--agent", self.agent_id,
            "--message", prompt,
            "--timeout", str(timeout)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout + 30,
                cwd=os.path.expanduser("~/.openclaw/workspace")
            )
            
            if result.returncode != 0:
                error_msg = result.stderr or "Unknown error"
                return f"❌ 调用失败: {error_msg}"
            
            return result.stdout
            
        except subprocess.TimeoutExpired:
            return f"⏱️ 调用 {self.name} 超时"
        except Exception as e:
            return f"❌ 调用 {self.name} 失败: {str(e)}"
    



# ============ Agent 工厂 ============
def get_agent(role: AgentRole) -> OpenClawAgent:
    """获取对应的 Agent"""
    return OpenClawAgent(role.value)


# ============ 任务执行 ============
class MultiAgentExecutor:
    """多 Agent 协同执行器"""
    
    def __init__(self, project_name: str, project_path: str = None):
        self.project_name = project_name
        self.project_path = project_path or f"~/Projects/{project_name}"
        self.results = {}
    
    def analyze_requirement(self, requirement: str) -> dict:
        """需求分析 - 产品经理"""
        print(f"\n📋 需求分析阶段")
        
        agent = get_agent(AgentRole.PRODUCT_MANAGER)
        
        prompt = f"""你是产品经理。请分析以下需求：

项目：{self.project_name}
项目路径：{self.project_path}

需求：{requirement}

请输出：
1. 需求概述
2. 用户故事（3-5条）
3. 功能列表（按优先级排序）
4. 核心业务流程
5. 需要注意的边界情况

请用中文回复。"""
        
        result = agent.call(prompt)
        self.results["product_manager"] = result
        return {"status": "ok", "result": result}
    
    def design_architecture(self, task: str) -> dict:
        """架构设计 - 架构师"""
        print(f"\n👨‍💻 架构设计阶段")
        
        agent = get_agent(AgentRole.ARCHITECT)
        
        prompt = f"""你是架构师。请设计以下模块的架构：

项目：{self.project_name}
项目路径：{self.project_path}

任务：{task}

请输出：
1. 技术选型建议
2. 模块划分
3. 数据库设计（如适用）
4. API 设计（如适用）
5. 架构图（用Mermaid格式）

请用中文回复。"""
        
        result = agent.call(prompt)
        self.results["architect"] = result
        return {"status": "ok", "result": result}
    
    def write_code(self, task: str) -> dict:
        """代码实现 - 软件工程师"""
        print(f"\n🧑‍💻 代码实现阶段")
        
        agent = get_agent(AgentRole.SOFTWARE_ENGINEER)
        
        prompt = f"""你是软件工程师。请实现以下功能：

项目：{self.project_name}
项目路径：{self.project_path}

任务：{task}

请：
1. 先了解项目结构和现有代码
2. 编写实现代码
3. 确保代码规范

请用中文回复，并给出完整的代码。"""
        
        result = agent.call(prompt, timeout=600)
        self.results["software_engineer"] = result
        return {"status": "ok", "result": result}
    
    def write_tests(self, task: str) -> dict:
        """测试用例 - 测试工程师"""
        print(f"\n🧪 测试阶段")
        
        agent = get_agent(AgentRole.TESTER)
        
        prompt = f"""你是测试工程师。请编写以下功能的测试用例：

项目：{self.project_name}
项目路径：{self.project_path}

任务：{task}

请输出：
1. 测试用例列表
2. 测试步骤
3. 预期结果
4. 边界条件

请用中文回复。"""
        
        result = agent.call(prompt)
        self.results["tester"] = result
        return {"status": "ok", "result": result}
    
    def design_ui(self, task: str) -> dict:
        """UI设计 - 交互设计师"""
        print(f"\n🎨 UI设计阶段")
        
        agent = get_agent(AgentRole.UI_DESIGNER)
        
        prompt = f"""你是交互设计师。请设计以下功能的界面：

项目：{self.project_name}
项目路径：{self.project_path}

任务：{task}

请输出：
1. 页面布局（可以用文字描述）
2. 交互流程
3. 组件建议
4. 用户体验要点

请用中文回复。"""
        
        result = agent.call(prompt)
        self.results["ui_designer"] = result
        return {"status": "ok", "result": result}
    
    def full_workflow(self, requirement: str) -> dict:
        """完整工作流：需求 -> 架构 -> 设计 -> 实现"""
        print(f"\n🚀 完整工作流启动")
        print(f"项目：{self.project_name}")
        print(f"需求：{requirement}")
        
        # 1. 需求分析
        self.analyze_requirement(requirement)
        
        # 2. 架构设计
        self.design_architecture(requirement)
        
        # 3. UI设计（可选）
        # self.design_ui(requirement)
        
        # 4. 代码实现
        # self.write_code(requirement)
        
        return {"status": "ok", "phases": list(self.results.keys())}


# ============ CLI ============
def main():
    parser = argparse.ArgumentParser(
        description="多 Agent 协同开发 (OpenClaw Agent 版)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
  # 需求分析（产品经理）
  python multi_agent_dev.py analyze --project castmind --requirement "实现用户登录"
  
  # 架构设计（架构师）
  python multi_agent_dev.py architect --project castmind --task "设计登录模块"
  
  # 代码实现（软件工程师）
  python multi_agent_dev.py code --project castmind --task "实现登录API"
  
  # 测试用例（测试工程师）
  python multi_agent_dev.py test --project castmind --task "登录模块测试"
  
  # UI设计（交互设计师）
  python multi_agent_dev.py design --project castmind --task "登录页面设计"
  
  # 完整工作流
  python multi_agent_dev.py run --project castmind --requirement "实现用户登录"
        """
    )
    
    parser.add_argument("--project", required=True, help="项目名称")
    parser.add_argument("--project-path", help="项目路径（默认：~/Projects/项目名）")
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # analyze 命令 - 需求分析
    analyze_parser = subparsers.add_parser("analyze", help="需求分析（产品经理）")
    analyze_parser.add_argument("--requirement", required=True, help="需求描述")
    
    # architect 命令 - 架构设计
    architect_parser = subparsers.add_parser("architect", help="架构设计（架构师）")
    architect_parser.add_argument("--task", required=True, help="任务描述")
    
    # code 命令 - 代码实现
    code_parser = subparsers.add_parser("code", help="代码实现（软件工程师）")
    code_parser.add_argument("--task", required=True, help="任务描述")
    
    # test 命令 - 测试用例
    test_parser = subparsers.add_parser("test", help="测试用例（测试工程师）")
    test_parser.add_argument("--task", required=True, help="任务描述")
    
    # design 命令 - UI设计
    design_parser = subparsers.add_parser("design", help="UI设计（交互设计师）")
    design_parser.add_argument("--task", required=True, help="任务描述")
    
    # run 命令 - 完整工作流
    run_parser = subparsers.add_parser("run", help="完整工作流")
    run_parser.add_argument("--requirement", required=True, help="需求描述")
    run_parser.add_argument("--skip-code", action="store_true", help="跳过代码实现")
    
    args = parser.parse_args()
    
    # 创建执行器
    executor = MultiAgentExecutor(
        project_name=args.project,
        project_path=args.project_path
    )
    
    # 执行对应命令
    if args.command == "analyze":
        result = executor.analyze_requirement(args.requirement)
        print(f"\n✅ 需求分析完成")
        
    elif args.command == "architect":
        result = executor.design_architecture(args.task)
        print(f"\n✅ 架构设计完成")
        
    elif args.command == "code":
        result = executor.write_code(args.task)
        print(f"\n✅ 代码实现完成")
        
    elif args.command == "test":
        result = executor.write_tests(args.task)
        print(f"\n✅ 测试用例完成")
        
    elif args.command == "design":
        result = executor.design_ui(args.task)
        print(f"\n✅ UI设计完成")
        
    elif args.command == "run":
        result = executor.full_workflow(args.requirement)
        print(f"\n✅ 完整工作流完成")
        print(f"已执行阶段：{', '.join(result.get('phases', []))}")
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
