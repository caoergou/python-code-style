"""机器人调度器

核心调度逻辑实现
这个模块实现了机器人任务调度的核心算法，展示了如何设计复杂业务逻辑的最佳实践。
"""

from models.robot import Robot, RobotStatus
from models.task import Task, TaskStatus


class SchedulerError(Exception):
    """调度器相关异常基类"""

    pass


class RobotNotFoundError(SchedulerError):
    """机器人未找到异常"""

    pass


class TaskNotFoundError(SchedulerError):
    """任务未找到异常"""

    pass


class RobotScheduler:
    """机器人调度器。

    负责管理机器人和任务，实现智能调度算法。
    展示了如何设计复杂的业务服务类。

    Attributes:
        robots: 注册的机器人字典，key为robot_id
        tasks: 系统中的任务字典，key为task_id
    """

    def __init__(self):
        """初始化调度器"""
        self.robots: dict[str, Robot] = {}
        self.tasks: dict[str, Task] = {}

    def register_robot(self, robot: Robot) -> None:
        """注册机器人到调度系统。

        Args:
            robot: 要注册的机器人实例

        Raises:
            SchedulerError: 当机器人ID已存在时
        """
        if robot.robot_id in self.robots:
            raise SchedulerError(f"机器人{robot.robot_id}已存在")

        self.robots[robot.robot_id] = robot

    def unregister_robot(self, robot_id: str) -> bool:
        """从系统中移除机器人。

        Args:
            robot_id: 机器人ID

        Returns:
            成功移除返回True，机器人不存在返回False
        """
        if robot_id not in self.robots:
            return False

        robot = self.robots[robot_id]
        if robot.current_task:
            # 如果机器人有任务，先释放任务
            task = self.tasks.get(robot.current_task)
            if task:
                task.status = TaskStatus.PENDING
                task.assigned_robot = None

        del self.robots[robot_id]
        return True

    def add_task(self, task: Task) -> None:
        """添加任务到调度系统。

        Args:
            task: 要添加的任务实例
        """
        self.tasks[task.task_id] = task

    def assign_task(self, task: Task) -> str | None:
        """为任务分配最适合的机器人。

        使用距离优先的简单调度算法：
        1. 找到所有可用的机器人
        2. 计算距离，选择最近的机器人
        3. 分配任务

        Args:
            task: 要分配的任务

        Returns:
            分配成功返回机器人ID，否则返回None
        """
        # 添加任务到系统
        self.add_task(task)

        # 找到最适合的机器人
        best_robot = self._find_best_robot(task)
        if not best_robot:
            return None

        # 分配任务
        try:
            best_robot.assign_task(task.task_id)
            task.assign_to_robot(best_robot.robot_id)
            return best_robot.robot_id
        except ValueError as e:
            # 如果分配失败，任务重新设为PENDING
            task.status = TaskStatus.PENDING
            task.assigned_robot = None
            raise SchedulerError("任务分配失败") from e

    def complete_task(self, task_id: str) -> bool:
        """完成指定任务。

        Args:
            task_id: 任务ID

        Returns:
            成功完成返回True，任务不存在返回False

        Raises:
            TaskNotFoundError: 当任务不存在时
        """
        task = self.tasks.get(task_id)
        if not task:
            raise TaskNotFoundError(f"任务{task_id}不存在")

        # 释放机器人
        if task.assigned_robot:
            robot = self.robots.get(task.assigned_robot)
            if robot:
                robot.complete_task()

        # 完成任务
        try:
            task.complete()
            return True
        except ValueError:
            # 任务状态不允许完成
            return False

    def fail_task(self, task_id: str, reason: str = "") -> bool:
        """标记任务失败。

        Args:
            task_id: 任务ID
            reason: 失败原因

        Returns:
            成功标记返回True，任务不存在返回False
        """
        task = self.tasks.get(task_id)
        if not task:
            return False

        # 释放机器人
        if task.assigned_robot:
            robot = self.robots.get(task.assigned_robot)
            if robot:
                robot.complete_task()

        # 标记任务失败
        task.fail(reason)
        return True

    def get_available_robots(self) -> list[Robot]:
        """获取所有可用的机器人。

        Returns:
            可用机器人列表
        """
        return [robot for robot in self.robots.values() if robot.is_available()]

    def get_pending_tasks(self) -> list[Task]:
        """获取所有待分配的任务。

        Returns:
            待分配任务列表，按优先级排序
        """
        pending_tasks = [task for task in self.tasks.values() if task.is_pending()]
        return sorted(pending_tasks, key=lambda t: t.priority, reverse=True)

    def get_system_status(self) -> dict[str, int]:
        """获取系统状态概览。

        Returns:
            包含系统状态信息的字典
        """
        total_robots = len(self.robots)
        idle_robots = len(
            [r for r in self.robots.values() if r.status == RobotStatus.IDLE]
        )
        busy_robots = len(
            [r for r in self.robots.values() if r.status == RobotStatus.BUSY]
        )

        total_tasks = len(self.tasks)
        pending_tasks = len([t for t in self.tasks.values() if t.is_pending()])
        completed_tasks = len([t for t in self.tasks.values() if t.is_completed()])

        return {
            "total_robots": total_robots,
            "idle_robots": idle_robots,
            "busy_robots": busy_robots,
            "charging_robots": len(
                [r for r in self.robots.values() if r.status == RobotStatus.CHARGING]
            ),
            "maintenance_robots": len(
                [r for r in self.robots.values() if r.status == RobotStatus.MAINTENANCE]
            ),
            "total_tasks": total_tasks,
            "pending_tasks": pending_tasks,
            "assigned_tasks": len(
                [t for t in self.tasks.values() if t.status == TaskStatus.ASSIGNED]
            ),
            "in_progress_tasks": len(
                [t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS]
            ),
            "completed_tasks": completed_tasks,
            "failed_tasks": len(
                [t for t in self.tasks.values() if t.status == TaskStatus.FAILED]
            ),
        }

    def _find_best_robot(self, task: Task) -> Robot | None:
        """找到执行指定任务的最佳机器人。

        当前使用简单的距离优先算法。

        Args:
            task: 要执行的任务

        Returns:
            最适合的机器人，如果没有可用机器人则返回None
        """
        available_robots = self.get_available_robots()
        if not available_robots:
            return None

        # 计算距离并找到最近的机器人
        best_robot = None
        min_distance = float("inf")

        for robot in available_robots:
            distance = robot.position.distance_to(task.target_position)
            if distance < min_distance:
                min_distance = distance
                best_robot = robot

        return best_robot

    def auto_assign_pending_tasks(self) -> dict[str, str | None]:
        """自动分配所有待分配的任务。

        Returns:
            分配结果字典，key为task_id，value为assigned_robot_id
        """
        assignments: dict[str, str | None] = {}
        pending_tasks = self.get_pending_tasks()

        for task in pending_tasks:
            try:
                assigned_robot = self.assign_task(task)
                if assigned_robot:
                    assignments[task.task_id] = assigned_robot
            except SchedulerError:
                # 跳过分配失败的任务
                continue

        return assignments
