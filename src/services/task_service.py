"""任务管理服务 - 展示服务层设计模式。

这个模块实现了任务管理的业务逻辑，
展示了如何设计清晰的服务层架构。
"""

import uuid

from models.robot import Position
from models.task import Task, TaskStatus, TaskType


class TaskService:
    """任务管理服务

    提供任务的创建、查询、更新等业务操作
    展示了如何将业务逻辑封装在服务层中
    """

    def __init__(self):
        """初始化任务服务"""
        self._tasks: dict[str, Task] = {}

    def create_task(
        self,
        task_type: TaskType,
        target_position: Position,
        priority: int = 1,
        estimated_duration: int = 30,
        description: str = "",
    ) -> Task:
        """创建新任务

        Args:
            task_type: 任务类型
            target_position: 目标位置
            priority: 优先级(1-5)
            estimated_duration: 预估执行时间(分钟)
            description: 任务描述

        Returns:
            创建的任务实例

        Raises:
            ValueError: 当参数不合法时
        """
        # 生成唯一任务ID
        task_id = f"T{uuid.uuid4().hex[:8].upper()}"

        # 创建任务
        task = Task(
            task_id=task_id,
            task_type=task_type,
            target_position=target_position,
            priority=priority,
            estimated_duration=estimated_duration,
            description=description,
        )

        # 存储任务
        self._tasks[task_id] = task

        return task

    def get_task(self, task_id: str) -> Task | None:
        """根据ID获取任务

        Args:
            task_id: 任务ID

        Returns:
            任务实例，如果不存在则返回None
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        """获取所有任务

        Returns:
            所有任务的列表
        """
        return list(self._tasks.values())

    def get_tasks_by_status(self, status: TaskStatus) -> list[Task]:
        """根据状态获取任务列表

        Args:
            status: 任务状态

        Returns:
            指定状态的任务列表
        """
        return [task for task in self._tasks.values() if task.status == status]

    def get_tasks_by_type(self, task_type: TaskType) -> list[Task]:
        """根据类型获取任务列表

        Args:
            task_type: 任务类型

        Returns:
            指定类型的任务列表
        """
        return [task for task in self._tasks.values() if task.task_type == task_type]

    def get_high_priority_tasks(self) -> list[Task]:
        """获取高优先级任务列表

        Returns:
            高优先级任务列表，按优先级排序
        """
        high_priority_tasks = [
            task for task in self._tasks.values() if task.is_high_priority()
        ]
        return sorted(high_priority_tasks, key=lambda t: t.priority, reverse=True)

    def get_pending_tasks(self) -> list[Task]:
        """获取待分配任务列表

        Returns:
            待分配任务列表，按优先级排序
        """
        pending_tasks = [task for task in self._tasks.values() if task.is_pending()]
        return sorted(pending_tasks, key=lambda t: t.priority, reverse=True)

    def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        """更新任务状态

        Args:
            task_id: 任务ID
            status: 新状态

        Returns:
            更新成功返回True，任务不存在返回False
        """
        task = self._tasks.get(task_id)
        if not task:
            return False

        task.status = status
        return True

    def delete_task(self, task_id: str) -> bool:
        """删除任务

        Args:
            task_id: 任务ID

        Returns:
            删除成功返回True，任务不存在返回False
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def get_task_statistics(self) -> dict[str, int]:
        """获取任务统计信息

        Returns:
            包含各种统计信息的字典
        """
        total_tasks = len(self._tasks)

        status_counts = {}
        for status in TaskStatus:
            status_counts[f"{status.value}_tasks"] = len(
                self.get_tasks_by_status(status)
            )

        type_counts = {}
        for task_type in TaskType:
            type_counts[f"{task_type.value}_tasks"] = len(
                self.get_tasks_by_type(task_type)
            )

        return {
            "total_tasks": total_tasks,
            "high_priority_tasks": len(self.get_high_priority_tasks()),
            **status_counts,
            **type_counts,
        }

    def create_delivery_task(
        self, target_position: Position, priority: int = 2, description: str = ""
    ) -> Task:
        """创建配送任务的便捷方法

        Args:
            target_position: 配送目标位置
            priority: 优先级
            description: 任务描述

        Returns:
            创建的配送任务
        """
        return self.create_task(
            task_type=TaskType.DELIVERY,
            target_position=target_position,
            priority=priority,
            estimated_duration=45,
            description=description or "配送任务",
        )

    def create_patrol_task(
        self, target_position: Position, priority: int = 1, description: str = ""
    ) -> Task:
        """创建巡逻任务的便捷方法

        Args:
            target_position: 巡逻目标位置
            priority: 优先级
            description: 任务描述

        Returns:
            创建的巡逻任务
        """
        return self.create_task(
            task_type=TaskType.PATROL,
            target_position=target_position,
            priority=priority,
            estimated_duration=60,
            description=description or "巡逻任务",
        )

    def create_cleaning_task(
        self, target_position: Position, priority: int = 3, description: str = ""
    ) -> Task:
        """创建清洁任务的便捷方法

        Args:
            target_position: 清洁目标位置
            priority: 优先级
            description: 任务描述

        Returns:
            创建的清洁任务
        """
        return self.create_task(
            task_type=TaskType.CLEANING,
            target_position=target_position,
            priority=priority,
            estimated_duration=90,
            description=description or "清洁任务",
        )
