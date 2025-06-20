"""Pytest配置和共享fixtures。

这个文件包含了测试中使用的共享fixtures，
展示了如何设计可复用的测试数据和工具。
"""

import pytest

from src.models.robot import Position, Robot, RobotStatus
from src.models.task import Task, TaskStatus, TaskType
from src.scheduler.robot_scheduler import RobotScheduler
from src.services.task_service import TaskService


@pytest.fixture
def sample_position() -> Position:
    """创建示例位置"""
    return Position(x=0.0, y=0.0)


@pytest.fixture
def target_position() -> Position:
    """创建目标位置"""
    return Position(x=10.0, y=5.0)


@pytest.fixture
def sample_robot(sample_position: Position) -> Robot:
    """创建示例机器人"""
    return Robot(
        robot_id="R001",
        name="测试机器人",
        position=sample_position,
        status=RobotStatus.IDLE,
        battery_level=100.0,
    )


@pytest.fixture
def low_battery_robot(sample_position: Position) -> Robot:
    """创建低电量机器人"""
    return Robot(
        robot_id="R002",
        name="低电量机器人",
        position=sample_position,
        status=RobotStatus.IDLE,
        battery_level=15.0,
    )


@pytest.fixture
def busy_robot(target_position: Position) -> Robot:
    """创建忙碌状态的机器人"""
    return Robot(
        robot_id="R003",
        name="忙碌机器人",
        position=target_position,
        status=RobotStatus.BUSY,
        current_task="T001",
        battery_level=80.0,
    )


@pytest.fixture
def sample_task(target_position: Position) -> Task:
    """创建示例任务"""
    return Task(
        task_id="T001",
        task_type=TaskType.DELIVERY,
        target_position=target_position,
        priority=2,
        status=TaskStatus.PENDING,
        estimated_duration=45,
        description="配送任务",
    )


@pytest.fixture
def high_priority_task(target_position: Position) -> Task:
    """创建高优先级任务"""
    return Task(
        task_id="T002",
        task_type=TaskType.CLEANING,
        target_position=target_position,
        priority=5,
        status=TaskStatus.PENDING,
        estimated_duration=90,
        description="紧急清洁任务",
    )


@pytest.fixture
def completed_task(target_position: Position) -> Task:
    """创建已完成任务"""
    return Task(
        task_id="T003",
        task_type=TaskType.PATROL,
        target_position=target_position,
        priority=1,
        status=TaskStatus.COMPLETED,
        estimated_duration=60,
        description="巡逻任务",
    )


@pytest.fixture
def robot_list(
    sample_robot: Robot, low_battery_robot: Robot, busy_robot: Robot
) -> list[Robot]:
    """创建机器人列表"""
    return [sample_robot, low_battery_robot, busy_robot]


@pytest.fixture
def task_list(
    sample_task: Task, high_priority_task: Task, completed_task: Task
) -> list[Task]:
    """创建任务列表"""
    return [sample_task, high_priority_task, completed_task]


@pytest.fixture
def empty_scheduler() -> RobotScheduler:
    """创建空的调度器"""
    return RobotScheduler()


@pytest.fixture
def scheduler_with_robots(
    empty_scheduler: RobotScheduler, robot_list: list[Robot]
) -> RobotScheduler:
    """创建带有机器人的调度器"""
    for robot in robot_list:
        # 重置机器人状态以便注册
        if robot.robot_id == "R003":  # busy_robot
            robot.status = RobotStatus.IDLE
            robot.current_task = None
        empty_scheduler.register_robot(robot)
    return empty_scheduler


@pytest.fixture
def task_service() -> TaskService:
    """创建任务服务实例"""
    return TaskService()


@pytest.fixture
def task_service_with_data(
    task_service: TaskService, task_list: list[Task]
) -> TaskService:
    """创建包含数据的任务服务"""
    for task in task_list:
        task_service._tasks[task.task_id] = task  # type: ignore
    return task_service


@pytest.fixture
def multiple_positions() -> list[Position]:
    """创建多个位置点"""
    return [
        Position(x=0, y=0),
        Position(x=5, y=5),
        Position(x=10, y=10),
        Position(x=-5, y=3),
        Position(x=8, y=-2),
    ]


@pytest.fixture
def delivery_positions() -> list[Position]:
    """创建配送点位置列表"""
    return [
        Position(x=10, y=5),
        Position(x=20, y=15),
        Position(x=-10, y=8),
        Position(x=0, y=25),
    ]


@pytest.fixture
def patrol_route() -> list[Position]:
    """创建巡逻路线"""
    return [
        Position(x=0, y=0),
        Position(x=10, y=0),
        Position(x=10, y=10),
        Position(x=0, y=10),
        Position(x=0, y=0),  # 回到起点
    ]
