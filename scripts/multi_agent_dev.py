#!/usr/bin/env python3
"""
多Agent协同开发脚本 - 支持任务状态保存
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


# ============ 配置 ============
SCRIPT_DIR = Path(__file__).parent
ARTIFACTS_DIR = SCRIPT_DIR.parent / "artifacts"
AGENT_BIN = os.path.expanduser("~/.nvm/versions/node/v22.22.0/bin/openclaw")


# ============ Agent 调用 ============
def call_agent(agent_id: str, prompt: str, timeout: int = 300) -> str:
    """调用 OpenClaw Agent"""
    cmd = [AGENT_BIN, "agent", "--agent", agent_id, "--message", prompt, "--timeout", str(timeout)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 30)
    return result.stdout if result.returncode == 0 else f"❌ Error: {result.stderr}"


# ============ 任务状态管理 ============
def save_task_status(project: str, phase: str, agent: str, status: str, result: str):
    """保存任务状态到JSON文件"""
    task_file = ARTIFACTS_DIR / f"{project}_tasks.json"
    
    # 读取现有任务
    tasks = {}
    if task_file.exists():
        with open(task_file, 'r') as f:
            tasks = json.load(f)
    
    # 更新任务状态
    if project not in tasks:
        tasks[project] = {"phases": {}, "updated_at": ""}
    
    tasks[project]["phases"][phase] = {
        "agent": agent,
        "status": status,  # pending, running, completed, failed
        "result": result,
        "timestamp": datetime.now().isoformat()
    }
    tasks[project]["updated_at"] = datetime.now().isoformat()
    
    # 保存
    task_file.parent.mkdir(parents=True, exist_ok=True)
    with open(task_file, 'w') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 任务状态已保存: {phase} -> {status}")


# ============ 主程序 ============
def main():
    parser = argparse.ArgumentParser(description="多Agent协同开发")
    parser.add_argument("--project", required=True, help="项目名称")
    parser.add_argument("--phase", choices=["analyze", "execute", "review", "coordinator"], 
                       default="coordinator", help="执行阶段")
    parser.add_argument("--requirement", help="需求描述")
    parser.add_argument("--task", help="任务描述")
    args = parser.parse_args()
    
    project = args.project
    phase = args.phase
    
    print(f"\n🚀 开始执行: {phase} 阶段")
    print(f"📁 项目: {project}")
    print("=" * 50)
    
    if phase == "analyze":
        # 需求分析阶段
        requirement = args.requirement or "分析项目需求"
        
        # 产品经理
        print("\n📋 调用产品经理...")
        save_task_status(project, "pm_analysis", "product-manager", "running", "")
        pm_prompt = f"你是产品经理。分析项目 {project} 的需求：{requirement}"
        pm_result = call_agent("product-manager", pm_prompt)
        print(pm_result)
        save_task_status(project, "pm_analysis", "product-manager", "completed", pm_result[:500])
        
        # 架构师
        print("\n👨‍💻 调用架构师...")
        save_task_status(project, "architecture", "architect", "running", "")
        arch_prompt = f"你是架构师。设计项目 {project} 的架构：{requirement}"
        arch_result = call_agent("architect", arch_prompt)
        print(arch_result)
        save_task_status(project, "architecture", "architect", "completed", arch_result[:500])
    
    elif phase == "execute":
        # 执行阶段
        task = args.task or "实现功能"
        
        # 软件工程师
        print("\n🧑‍💻 调用软件工程师...")
        save_task_status(project, "code", "software-engineer", "running", "")
        code_prompt = f"你是软件工程师。在项目 {project} 中：{task}"
        code_result = call_agent("software-engineer", code_prompt, timeout=600)
        print(code_result)
        save_task_status(project, "code", "software-engineer", "completed", code_result[:500])
    
    elif phase == "review":
        # 审查阶段
        task = args.task or "审查代码"
        
        # 测试工程师
        print("\n🧪 调用测试工程师...")
        save_task_status(project, "test", "tester", "running", "")
        test_prompt = f"你是测试工程师。为项目 {project} 编写测试用例：{task}"
        test_result = call_agent("tester", test_prompt)
        print(test_result)
        save_task_status(project, "test", "tester", "completed", test_result[:500])
    
    elif phase == "coordinator":
        # 完整流程
        requirement = args.requirement or args.task or "完成项目开发"
        
        phases = [
            ("pm_analysis", "product-manager", "需求分析", f"分析项目需求：{requirement}"),
            ("architecture", "architect", "架构设计", f"设计项目架构：{requirement}"),
            ("code", "software-engineer", "代码实现", f"实现功能：{requirement}"),
            ("test", "tester", "测试用例", f"编写测试：{requirement}"),
        ]
        
        for phase_id, agent_id, phase_name, prompt in phases:
            print(f"\n{'='*50}")
            print(f"📋 阶段: {phase_name}")
            print(f"{'='*50}")
            
            save_task_status(project, phase_id, agent_id, "running", "")
            result = call_agent(agent_id, f"你是{phase_name}。{prompt}", timeout=600)
            print(result)
            save_task_status(project, phase_id, agent_id, "completed", result[:500])
    
    print(f"\n{'='*50}")
    print(f"✅ {phase} 阶段执行完成！")
    print(f"📁 任务状态保存在: artifacts/{project}_tasks.json")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
