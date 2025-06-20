"""基本使用示例 - 展示机器人调度系统的主要功能"""

from models.robot import Position, Robot
from models.task import Task, TaskType
from scheduler.robot_scheduler import RobotScheduler


def main():
    """主演示函数"""
    print("🤖 机器人调度系统演示")
    print("=" * 50)

    # 创建调度器
    scheduler = RobotScheduler()

    # 创建机器人
    robot = Robot(robot_id="R001", name="演示机器人", position=Position(x=0, y=0))

    # 注册机器人
    scheduler.register_robot(robot)
    print(f"✅ 注册机器人: {robot.name}")

    # 创建任务
    task = Task(
        task_id="T001",
        task_type=TaskType.DELIVERY,
        target_position=Position(x=10, y=5),
        description="配送任务",
    )

    # 分配任务
    assigned_robot = scheduler.assign_task(task)
    if assigned_robot:
        print(f"✅ 任务分配成功: {task.description} -> {robot.name}")
    else:
        print("❌ 任务分配失败")

    # 显示状态
    status = scheduler.get_system_status()
    print(f"📊 系统状态: {status}")

    print("✅ 演示完成!")


if __name__ == "__main__":
    main()
