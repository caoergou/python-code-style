"""数据模型包 - 使用Pydantic实现数据验证和建模。

这个包包含了机器人调度系统的所有数据模型：
- Robot: 机器人实体模型
- Task: 任务实体模型
- Position: 位置坐标模型
"""

from .robot import Position, Robot, RobotStatus
from .task import Task, TaskStatus, TaskType

__all__ = [
    "Robot",
    "RobotStatus",
    "Position",
    "Task",
    "TaskType",
    "TaskStatus",
]
