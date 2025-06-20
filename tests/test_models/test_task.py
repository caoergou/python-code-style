"""任务模型测试 - 展示任务业务逻辑测试。

这个模块测试任务模型的所有功能，
包括状态管理、验证和业务方法。
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from src.models.robot import Position
from src.models.task import Task, TaskStatus, TaskType


class TestTask:
    """任务模型测试类"""

    def test_create_valid_task(self, target_position: Position):
        """测试创建有效任务"""
        task = Task(
            task_id="T001",
            task_type=TaskType.DELIVERY,
            target_position=target_position,
            priority=3,
            estimated_duration=45,
            description="配送任务",
        )

        assert task.task_id == "T001"
        assert task.task_type == TaskType.DELIVERY
        assert task.target_position == target_position
        assert task.priority == 3
        assert task.estimated_duration == 45
        assert task.description == "配送任务"
        assert task.status == TaskStatus.PENDING
        assert task.assigned_robot is None
        assert isinstance(task.created_at, datetime)

    def test_task_id_validation(self, target_position: Position):
        """测试任务ID验证"""
        # 测试无效ID（不以T开头）
        with pytest.raises(ValidationError) as exc_info:
            Task(
                task_id="INVALID001",
                task_type=TaskType.DELIVERY,
                target_position=target_position,
            )
        assert "任务ID必须以T开头" in str(exc_info.value)

        # 测试空ID
        with pytest.raises(ValidationError):
            Task(
                task_id="",
                task_type=TaskType.DELIVERY,
                target_position=target_position,
            )

    def test_priority_validation(self, target_position: Position):
        """测试优先级验证"""
        # 测试优先级过低
        with pytest.raises(ValidationError):
            Task(
                task_id="T001",
                task_type=TaskType.DELIVERY,
                target_position=target_position,
                priority=0,
            )

        # 测试优先级过高
        with pytest.raises(ValidationError):
            Task(
                task_id="T001",
                task_type=TaskType.DELIVERY,
                target_position=target_position,
                priority=6,
            )

        # 测试有效优先级
        for priority in range(1, 6):
            task = Task(
                task_id=f"T{priority:03d}",
                task_type=TaskType.DELIVERY,
                target_position=target_position,
                priority=priority,
            )
            assert task.priority == priority

    def test_estimated_duration_validation(self, target_position: Position):
        """测试预估时间验证"""
        # 测试负数时间
        with pytest.raises(ValidationError):
            Task(
                task_id="T001",
                task_type=TaskType.DELIVERY,
                target_position=target_position,
                estimated_duration=-1,
            )

        # 测试零时间
        with pytest.raises(ValidationError):
            Task(
                task_id="T001",
                task_type=TaskType.DELIVERY,
                target_position=target_position,
                estimated_duration=0,
            )

    def test_task_status_methods(self, sample_task: Task):
        """测试任务状态判断方法"""
        # 测试待分配状态
        assert sample_task.is_pending() is True
        assert sample_task.is_completed() is False

        # 测试已分配状态
        sample_task.status = TaskStatus.ASSIGNED
        assert sample_task.is_pending() is False

        # 测试进行中状态
        sample_task.status = TaskStatus.IN_PROGRESS
        assert sample_task.is_pending() is False
        assert sample_task.is_completed() is False

        # 测试已完成状态
        sample_task.status = TaskStatus.COMPLETED
        assert sample_task.is_completed() is True
        assert sample_task.is_pending() is False

        # 测试失败状态
        sample_task.status = TaskStatus.FAILED
        assert sample_task.is_pending() is False
        assert sample_task.is_completed() is False

    def test_is_high_priority(self, target_position: Position):
        """测试高优先级判断"""
        # 测试低优先级任务
        low_priority_task = Task(
            task_id="T001",
            task_type=TaskType.PATROL,
            target_position=target_position,
            priority=2,
        )
        assert low_priority_task.is_high_priority() is False

        # 测试高优先级任务
        high_priority_task = Task(
            task_id="T002",
            task_type=TaskType.CLEANING,
            target_position=target_position,
            priority=4,
        )
        assert high_priority_task.is_high_priority() is True

        # 测试边界值
        medium_priority_task = Task(
            task_id="T003",
            task_type=TaskType.DELIVERY,
            target_position=target_position,
            priority=3,
        )
        assert medium_priority_task.is_high_priority() is False

    def test_assign_to_robot(self, sample_task: Task):
        """测试分配给机器人"""
        # 测试成功分配
        sample_task.assign_to_robot("R001")
        assert sample_task.assigned_robot == "R001"
        assert sample_task.status == TaskStatus.ASSIGNED

        # 测试重复分配
        with pytest.raises(ValueError) as exc_info:
            sample_task.assign_to_robot("R002")
        assert "无法分配" in str(exc_info.value)

    def test_start_execution(self, sample_task: Task):
        """测试开始执行任务"""
        # 测试从待分配直接开始执行（应该失败）
        with pytest.raises(ValueError) as exc_info:
            sample_task.start_execution()
        assert "无法开始执行" in str(exc_info.value)

        # 测试正常流程
        sample_task.assign_to_robot("R001")
        sample_task.start_execution()
        assert sample_task.status == TaskStatus.IN_PROGRESS

    def test_complete_task(self, sample_task: Task):
        """测试完成任务"""
        # 测试从待分配直接完成（应该失败）
        with pytest.raises(ValueError) as exc_info:
            sample_task.complete()
        assert "无法完成" in str(exc_info.value)

        # 测试正常流程
        sample_task.assign_to_robot("R001")
        sample_task.start_execution()
        sample_task.complete()
        assert sample_task.status == TaskStatus.COMPLETED

    def test_fail_task(self, sample_task: Task):
        """测试任务失败"""
        sample_task.assign_to_robot("R001")
        sample_task.start_execution()

        # 测试任务失败
        sample_task.fail("机器人故障")
        assert sample_task.status == TaskStatus.FAILED

    def test_task_types(self, target_position: Position):
        """测试所有任务类型"""
        for task_type in TaskType:
            task = Task(
                task_id=f"T{task_type.value.upper()}001",
                task_type=task_type,
                target_position=target_position,
            )
            assert task.task_type == task_type

    def test_task_serialization(self, sample_task: Task):
        """测试任务序列化"""
        data = sample_task.model_dump()

        assert data["task_id"] == "T001"
        assert data["task_type"] == "delivery"
        assert data["priority"] == 2
        assert data["status"] == "pending"
        assert "target_position" in data

    def test_task_json_export_import(self, sample_task: Task):
        """测试JSON导出和导入"""
        # 导出为JSON
        json_str = sample_task.model_dump_json()
        assert "T001" in json_str
        assert "delivery" in json_str

        # 从JSON导入
        data = sample_task.model_dump()
        new_task = Task(**data)

        assert new_task.task_id == sample_task.task_id
        assert new_task.task_type == sample_task.task_type
        assert new_task.priority == sample_task.priority

    def test_task_edge_cases(self, target_position: Position):
        """测试边界情况"""
        # 测试最短估计时间
        task = Task(
            task_id="T001",
            task_type=TaskType.DELIVERY,
            target_position=target_position,
            estimated_duration=1,
        )
        assert task.estimated_duration == 1

        # 测试最长描述
        long_description = "A" * 500
        task = Task(
            task_id="T002",
            task_type=TaskType.PATROL,
            target_position=target_position,
            description=long_description,
        )
        assert task.description == long_description

        # 测试最高优先级
        task = Task(
            task_id="T003",
            task_type=TaskType.CLEANING,
            target_position=target_position,
            priority=5,
        )
        assert task.priority == 5
        assert task.is_high_priority() is True
