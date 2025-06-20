"""任务服务测试 - 展示服务层业务逻辑测试

这个模块测试任务服务的所有业务功能，
包括任务管理、查询和统计功能。
"""

from src.models.robot import Position
from src.models.task import Task, TaskStatus, TaskType
from src.services.task_service import TaskService


class TestTaskService:
    """任务服务测试类"""

    def test_create_task(self, task_service: TaskService, target_position: Position):
        """测试创建任务"""
        task = task_service.create_task(
            task_type=TaskType.DELIVERY,
            target_position=target_position,
            priority=3,
            estimated_duration=45,
            description="测试配送任务",
        )

        assert task.task_type == TaskType.DELIVERY
        assert task.target_position == target_position
        assert task.priority == 3
        assert task.estimated_duration == 45
        assert task.description == "测试配送任务"
        assert task.status == TaskStatus.PENDING
        assert task.task_id.startswith("T")

        # 验证任务已存储
        stored_task = task_service.get_task(task.task_id)
        assert stored_task == task

    def test_create_task_with_defaults(
        self, task_service: TaskService, target_position: Position
    ):
        """测试使用默认参数创建任务"""
        task = task_service.create_task(
            task_type=TaskType.PATROL,
            target_position=target_position,
        )

        assert task.priority == 1
        assert task.estimated_duration == 30
        assert task.description == ""

    def test_get_task_existing(
        self, task_service_with_data: TaskService, sample_task: Task
    ):
        """测试获取存在的任务"""
        task = task_service_with_data.get_task(sample_task.task_id)
        assert task == sample_task

    def test_get_task_non_existing(self, task_service: TaskService):
        """测试获取不存在的任务"""
        task = task_service.get_task("NONEXISTENT")
        assert task is None

    def test_get_all_tasks(
        self, task_service_with_data: TaskService, task_list: list[Task]
    ):
        """测试获取所有任务"""
        all_tasks = task_service_with_data.get_all_tasks()
        assert len(all_tasks) == len(task_list)

        # 验证所有任务都存在
        task_ids = {task.task_id for task in all_tasks}
        expected_ids = {task.task_id for task in task_list}
        assert task_ids == expected_ids

    def test_get_tasks_by_status(self, task_service_with_data: TaskService):
        """测试按状态获取任务"""
        pending_tasks = task_service_with_data.get_tasks_by_status(TaskStatus.PENDING)
        assert len(pending_tasks) == 2  # sample_task和high_priority_task

        completed_tasks = task_service_with_data.get_tasks_by_status(
            TaskStatus.COMPLETED
        )
        assert len(completed_tasks) == 1  # completed_task

        failed_tasks = task_service_with_data.get_tasks_by_status(TaskStatus.FAILED)
        assert len(failed_tasks) == 0

    def test_get_tasks_by_type(self, task_service_with_data: TaskService):
        """测试按类型获取任务"""
        delivery_tasks = task_service_with_data.get_tasks_by_type(TaskType.DELIVERY)
        assert len(delivery_tasks) == 1

        cleaning_tasks = task_service_with_data.get_tasks_by_type(TaskType.CLEANING)
        assert len(cleaning_tasks) == 1

        patrol_tasks = task_service_with_data.get_tasks_by_type(TaskType.PATROL)
        assert len(patrol_tasks) == 1

    def test_get_high_priority_tasks(
        self, task_service_with_data: TaskService, high_priority_task: Task
    ):
        """测试获取高优先级任务"""
        high_priority_tasks = task_service_with_data.get_high_priority_tasks()
        assert len(high_priority_tasks) == 1
        assert high_priority_tasks[0] == high_priority_task

    def test_get_pending_tasks(self, task_service_with_data: TaskService):
        """测试获取待分配任务"""
        pending_tasks = task_service_with_data.get_pending_tasks()
        assert len(pending_tasks) == 2

        # 验证按优先级排序（高优先级在前）
        assert pending_tasks[0].priority >= pending_tasks[1].priority

    def test_update_task_status_existing(
        self, task_service_with_data: TaskService, sample_task: Task
    ):
        """测试更新存在任务的状态"""
        success = task_service_with_data.update_task_status(
            sample_task.task_id, TaskStatus.ASSIGNED
        )
        assert success is True

        updated_task = task_service_with_data.get_task(sample_task.task_id)
        assert updated_task is not None
        assert updated_task.status == TaskStatus.ASSIGNED

    def test_update_task_status_non_existing(self, task_service: TaskService):
        """测试更新不存在任务的状态"""
        success = task_service.update_task_status("NONEXISTENT", TaskStatus.ASSIGNED)
        assert success is False

    def test_delete_task_existing(
        self, task_service_with_data: TaskService, sample_task: Task
    ):
        """测试删除存在的任务"""
        success = task_service_with_data.delete_task(sample_task.task_id)
        assert success is True

        deleted_task = task_service_with_data.get_task(sample_task.task_id)
        assert deleted_task is None

    def test_delete_task_non_existing(self, task_service: TaskService):
        """测试删除不存在的任务"""
        success = task_service.delete_task("NONEXISTENT")
        assert success is False

    def test_get_task_statistics_empty(self, task_service: TaskService):
        """测试空服务的统计信息"""
        stats = task_service.get_task_statistics()

        assert stats["total_tasks"] == 0
        assert stats["high_priority_tasks"] == 0
        assert stats["pending_tasks"] == 0
        assert stats["assigned_tasks"] == 0
        assert stats["in_progress_tasks"] == 0
        assert stats["completed_tasks"] == 0
        assert stats["failed_tasks"] == 0
        assert stats["delivery_tasks"] == 0
        assert stats["patrol_tasks"] == 0
        assert stats["cleaning_tasks"] == 0

    def test_get_task_statistics_with_data(self, task_service_with_data: TaskService):
        """测试有数据的统计信息"""
        stats = task_service_with_data.get_task_statistics()

        assert stats["total_tasks"] == 3
        assert stats["high_priority_tasks"] == 1
        assert stats["pending_tasks"] == 2
        assert stats["completed_tasks"] == 1
        assert stats["delivery_tasks"] == 1
        assert stats["patrol_tasks"] == 1
        assert stats["cleaning_tasks"] == 1

    def test_create_delivery_task(
        self, task_service: TaskService, target_position: Position
    ):
        """测试创建配送任务便捷方法"""
        task = task_service.create_delivery_task(
            target_position=target_position,
            priority=3,
            description="测试配送",
        )

        assert task.task_type == TaskType.DELIVERY
        assert task.priority == 3
        assert task.estimated_duration == 45
        assert task.description == "测试配送"

    def test_create_delivery_task_defaults(
        self, task_service: TaskService, target_position: Position
    ):
        """测试创建配送任务使用默认值"""
        task = task_service.create_delivery_task(target_position)

        assert task.task_type == TaskType.DELIVERY
        assert task.priority == 2
        assert task.estimated_duration == 45
        assert task.description == "配送任务"

    def test_create_patrol_task(
        self, task_service: TaskService, target_position: Position
    ):
        """测试创建巡逻任务便捷方法"""
        task = task_service.create_patrol_task(
            target_position=target_position,
            priority=2,
            description="测试巡逻",
        )

        assert task.task_type == TaskType.PATROL
        assert task.priority == 2
        assert task.estimated_duration == 60
        assert task.description == "测试巡逻"

    def test_create_cleaning_task(
        self, task_service: TaskService, target_position: Position
    ):
        """测试创建清洁任务便捷方法"""
        task = task_service.create_cleaning_task(
            target_position=target_position,
            priority=4,
            description="测试清洁",
        )

        assert task.task_type == TaskType.CLEANING
        assert task.priority == 4
        assert task.estimated_duration == 90
        assert task.description == "测试清洁"

    def test_multiple_task_creation(
        self, task_service: TaskService, target_position: Position
    ):
        """测试批量创建任务"""
        task_count = 5
        tasks: list[Task] = []

        for i in range(task_count):
            task = task_service.create_task(
                task_type=TaskType.DELIVERY,
                target_position=target_position,
                priority=1,
                description=f"批量任务{i}",
            )
            tasks.append(task)

        # 验证所有任务都有唯一ID
        task_ids = [task.task_id for task in tasks]
        assert len(set(task_ids)) == task_count

        # 验证都已存储
        all_tasks = task_service.get_all_tasks()
        assert len(all_tasks) == task_count

    def test_task_id_generation(
        self, task_service: TaskService, target_position: Position
    ):
        """测试任务ID生成的唯一性"""
        task_ids: set[str] = set()

        for _ in range(10):
            task = task_service.create_task(
                task_type=TaskType.PATROL,
                target_position=target_position,
            )
            task_ids.add(task.task_id)

        # 所有ID应该唯一
        assert len(task_ids) == 10

        # 所有ID应该以T开头
        for task_id in task_ids:
            assert task_id.startswith("T")
