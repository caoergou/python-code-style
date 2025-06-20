"""机器人调度器测试 - 展示复杂业务逻辑测试。

这个模块测试调度器的所有功能，
包括机器人管理、任务分配和调度算法。
"""

import pytest

from src.models.robot import Position, Robot, RobotStatus
from src.models.task import Task, TaskStatus, TaskType
from src.scheduler.robot_scheduler import (
    RobotScheduler,
    SchedulerError,
    TaskNotFoundError,
)


class TestRobotScheduler:
    """机器人调度器测试类"""

    def test_register_robot(self, empty_scheduler: RobotScheduler, sample_robot: Robot):
        """测试注册机器人"""
        empty_scheduler.register_robot(sample_robot)

        assert sample_robot.robot_id in empty_scheduler.robots
        assert empty_scheduler.robots[sample_robot.robot_id] == sample_robot

    def test_register_duplicate_robot(
        self, empty_scheduler: RobotScheduler, sample_robot: Robot
    ):
        """测试注册重复机器人"""
        empty_scheduler.register_robot(sample_robot)

        with pytest.raises(SchedulerError) as exc_info:
            empty_scheduler.register_robot(sample_robot)
        assert "已存在" in str(exc_info.value)

    def test_unregister_robot_existing(
        self, scheduler_with_robots: RobotScheduler, sample_robot: Robot
    ):
        """测试移除存在的机器人"""
        success = scheduler_with_robots.unregister_robot(sample_robot.robot_id)
        assert success is True
        assert sample_robot.robot_id not in scheduler_with_robots.robots

    def test_unregister_robot_non_existing(self, empty_scheduler: RobotScheduler):
        """测试移除不存在的机器人"""
        success = empty_scheduler.unregister_robot("NONEXISTENT")
        assert success is False

    def test_unregister_robot_with_task(
        self, empty_scheduler: RobotScheduler, sample_robot: Robot, sample_task: Task
    ):
        """测试移除有任务的机器人"""
        # 注册机器人并分配任务
        empty_scheduler.register_robot(sample_robot)
        empty_scheduler.add_task(sample_task)

        # 模拟分配任务
        sample_robot.assign_task(sample_task.task_id)
        sample_task.assign_to_robot(sample_robot.robot_id)

        # 移除机器人
        success = empty_scheduler.unregister_robot(sample_robot.robot_id)
        assert success is True

        # 验证任务状态重置
        assert sample_task.status == TaskStatus.PENDING
        assert sample_task.assigned_robot is None

    def test_add_task(self, empty_scheduler: RobotScheduler, sample_task: Task):
        """测试添加任务"""
        empty_scheduler.add_task(sample_task)

        assert sample_task.task_id in empty_scheduler.tasks
        assert empty_scheduler.tasks[sample_task.task_id] == sample_task

    def test_assign_task_success(
        self, scheduler_with_robots: RobotScheduler, sample_task: Task
    ):
        """测试成功分配任务"""
        assigned_robot_id = scheduler_with_robots.assign_task(sample_task)

        assert assigned_robot_id is not None
        assert sample_task.status == TaskStatus.ASSIGNED
        assert sample_task.assigned_robot == assigned_robot_id

        # 验证机器人状态
        robot = scheduler_with_robots.robots[assigned_robot_id]
        assert robot.status == RobotStatus.BUSY
        assert robot.current_task == sample_task.task_id

    def test_assign_task_no_available_robots(
        self, empty_scheduler: RobotScheduler, sample_task: Task
    ):
        """测试没有可用机器人时分配任务"""
        assigned_robot_id = empty_scheduler.assign_task(sample_task)

        assert assigned_robot_id is None
        assert sample_task.status == TaskStatus.PENDING

    def test_assign_task_distance_priority(
        self, empty_scheduler: RobotScheduler, multiple_positions: list[Position]
    ):
        """测试基于距离的任务分配优先级"""
        # 创建多个机器人在不同位置
        robots: list[Robot] = []
        for i, pos in enumerate(multiple_positions[:3]):
            robot = Robot(
                robot_id=f"R{i:03d}",
                name=f"机器人{i}",
                position=pos,
            )
            robots.append(robot)
            empty_scheduler.register_robot(robot)

        # 创建任务在最后一个位置
        target_pos = multiple_positions[-1]
        task = Task(
            task_id="T001",
            task_type=TaskType.DELIVERY,
            target_position=target_pos,
        )

        # 分配任务
        assigned_robot_id = empty_scheduler.assign_task(task)

        # 找到最近的机器人
        closest_robot = None
        min_distance = float("inf")
        for robot in robots:
            distance = robot.position.distance_to(target_pos)
            if distance < min_distance:
                min_distance = distance
                closest_robot = robot

        assert assigned_robot_id == closest_robot.robot_id if closest_robot else None

    def test_complete_task_success(
        self, scheduler_with_robots: RobotScheduler, sample_task: Task
    ):
        """测试成功完成任务"""
        # 先分配任务
        assigned_robot_id = scheduler_with_robots.assign_task(sample_task)
        sample_task.start_execution()

        # 完成任务
        success = scheduler_with_robots.complete_task(sample_task.task_id)
        assert success is True

        # 验证状态
        assert sample_task.status == TaskStatus.COMPLETED
        if assigned_robot_id:
            robot = scheduler_with_robots.robots[assigned_robot_id]
            assert robot.status == RobotStatus.IDLE
            assert robot.current_task is None

    def test_complete_task_non_existing(self, empty_scheduler: RobotScheduler):
        """测试完成不存在的任务"""
        with pytest.raises(TaskNotFoundError):
            empty_scheduler.complete_task("NONEXISTENT")

    def test_fail_task_success(
        self, scheduler_with_robots: RobotScheduler, sample_task: Task
    ):
        """测试任务失败处理"""
        # 先分配任务
        assigned_robot_id = scheduler_with_robots.assign_task(sample_task)
        sample_task.start_execution()

        # 标记任务失败
        success = scheduler_with_robots.fail_task(sample_task.task_id, "机器人故障")
        assert success is True

        # 验证状态
        assert sample_task.status == TaskStatus.FAILED
        if assigned_robot_id:
            robot = scheduler_with_robots.robots[assigned_robot_id]
            assert robot.status == RobotStatus.IDLE
            assert robot.current_task is None

    def test_fail_task_non_existing(self, empty_scheduler: RobotScheduler):
        """测试标记不存在任务失败"""
        success = empty_scheduler.fail_task("NONEXISTENT")
        assert success is False

    def test_get_available_robots(self, scheduler_with_robots: RobotScheduler):
        """测试获取可用机器人"""
        available_robots = scheduler_with_robots.get_available_robots()

        # 应该有可用机器人（sample_robot肯定可用，其他取决于配置）
        # 注意：low_battery_robot电量15%，低于20%阈值，不可用
        assert len(available_robots) >= 1

        # 验证都是可用状态
        for robot in available_robots:
            assert robot.is_available() is True

    def test_get_pending_tasks(
        self, empty_scheduler: RobotScheduler, task_list: list[Task]
    ):
        """测试获取待分配任务"""
        # 添加任务（只有pending状态的任务）
        pending_tasks_count = 0
        for task in task_list:
            empty_scheduler.add_task(task)
            if task.is_pending():
                pending_tasks_count += 1

        pending_tasks = empty_scheduler.get_pending_tasks()
        assert len(pending_tasks) == pending_tasks_count

        # 验证按优先级排序
        for i in range(len(pending_tasks) - 1):
            assert pending_tasks[i].priority >= pending_tasks[i + 1].priority

    def test_get_system_status_empty(self, empty_scheduler: RobotScheduler):
        """测试空系统状态"""
        status = empty_scheduler.get_system_status()

        assert status["total_robots"] == 0
        assert status["idle_robots"] == 0
        assert status["busy_robots"] == 0
        assert status["charging_robots"] == 0
        assert status["maintenance_robots"] == 0
        assert status["total_tasks"] == 0
        assert status["pending_tasks"] == 0
        assert status["assigned_tasks"] == 0
        assert status["in_progress_tasks"] == 0
        assert status["completed_tasks"] == 0
        assert status["failed_tasks"] == 0

    def test_get_system_status_with_data(
        self, scheduler_with_robots: RobotScheduler, task_list: list[Task]
    ):
        """测试有数据的系统状态"""
        # 添加任务
        for task in task_list:
            scheduler_with_robots.add_task(task)

        status = scheduler_with_robots.get_system_status()

        assert status["total_robots"] == 3
        assert status["idle_robots"] >= 1
        assert status["total_tasks"] == len(task_list)
        assert status["pending_tasks"] >= 1
        assert status["completed_tasks"] >= 1

    def test_auto_assign_pending_tasks(self, scheduler_with_robots: RobotScheduler):
        """测试自动分配待分配任务"""
        # 创建多个待分配任务
        tasks: list[Task] = []
        for i in range(3):
            task = Task(
                task_id=f"T{i:03d}",
                task_type=TaskType.DELIVERY,
                target_position=Position(x=i * 10, y=i * 10),
                priority=i + 1,
            )
            tasks.append(task)
            scheduler_with_robots.add_task(task)

        # 自动分配
        assignments = scheduler_with_robots.auto_assign_pending_tasks()

        # 验证分配结果
        assert len(assignments) > 0

        for task_id, robot_id in assignments.items():
            if robot_id:  # 成功分配的任务
                task = scheduler_with_robots.tasks[task_id]
                assert task.status == TaskStatus.ASSIGNED
                assert task.assigned_robot == robot_id

    def test_scheduler_error_handling(
        self, scheduler_with_robots: RobotScheduler, sample_task: Task
    ):
        """测试调度器错误处理"""
        # 分配任务给繁忙的机器人应该抛出异常
        assigned_robot_id = scheduler_with_robots.assign_task(sample_task)
        robot = scheduler_with_robots.robots[assigned_robot_id]  # type: ignore

        # 尝试再次分配任务给同一个机器人
        another_task = Task(
            task_id="T999",
            task_type=TaskType.CLEANING,
            target_position=Position(x=100, y=100),
        )

        # 手动设置机器人为繁忙状态来测试错误处理
        with pytest.raises(ValueError):
            robot.assign_task(another_task.task_id)  # 这应该抛出ValueError

    def test_robot_scheduler_integration(
        self, empty_scheduler: RobotScheduler, delivery_positions: list[Position]
    ):
        """测试调度器完整工作流程"""
        # 1. 注册多个机器人
        robots: list[Robot] = []
        for i in range(3):
            robot = Robot(
                robot_id=f"R{i:03d}",
                name=f"配送机器人{i}",
                position=Position(x=0, y=0),
                battery_level=80 + i * 5,
            )
            robots.append(robot)
            empty_scheduler.register_robot(robot)

        # 2. 创建多个任务
        tasks: list[Task] = []
        for i, pos in enumerate(delivery_positions):
            task = Task(
                task_id=f"T{i:03d}",
                task_type=TaskType.DELIVERY,
                target_position=pos,
                priority=5 - i,  # 递减优先级
            )
            tasks.append(task)

        # 3. 分配任务
        assignments: dict[str, str] = {}
        for task in tasks:
            robot_id = empty_scheduler.assign_task(task)
            if robot_id:
                assignments[task.task_id] = robot_id

        # 4. 验证分配结果
        assert len(assignments) > 0

        # 5. 开始执行部分任务
        executed_tasks: list[str] = []
        for task_id in list(assignments.keys())[:2]:
            task = empty_scheduler.tasks[task_id]
            task.start_execution()
            executed_tasks.append(task_id)

        # 6. 完成一个任务
        if executed_tasks:
            success = empty_scheduler.complete_task(executed_tasks[0])
            assert success is True

        # 7. 验证系统状态
        status = empty_scheduler.get_system_status()
        assert status["total_robots"] == 3
        assert status["total_tasks"] == len(tasks)
        assert status["completed_tasks"] >= 1
