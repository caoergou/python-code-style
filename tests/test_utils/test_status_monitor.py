"""测试状态监控器功能"""

from src.models.robot import Position, Robot, RobotStatus
from src.models.task import Task, TaskStatus, TaskType
from src.utils.status_monitor import StatusMonitor


class TestStatusMonitor:
    """测试状态监控器"""

    def setup_method(self):
        """测试前的准备工作"""
        self.monitor = StatusMonitor()

    def test_get_robot_utilization_empty_list(self):
        """测试空机器人列表的利用率计算"""
        result = self.monitor.get_robot_utilization([])
        assert result == {}

    def test_get_robot_utilization_normal(self):
        """测试正常机器人利用率计算"""
        robots = [
            Robot(
                robot_id="R1",
                name="Robot1",
                position=Position(x=0, y=0),
                status=RobotStatus.IDLE,
            ),
            Robot(
                robot_id="R2",
                name="Robot2",
                position=Position(x=1, y=1),
                status=RobotStatus.BUSY,
            ),
            Robot(
                robot_id="R3",
                name="Robot3",
                position=Position(x=2, y=2),
                status=RobotStatus.CHARGING,
            ),
            Robot(
                robot_id="R4",
                name="Robot4",
                position=Position(x=3, y=3),
                status=RobotStatus.MAINTENANCE,
            ),
        ]

        result = self.monitor.get_robot_utilization(robots)

        assert result["total_robots"] == 4
        assert result["idle_rate"] == 25.0
        assert result["busy_rate"] == 25.0
        assert result["charging_rate"] == 25.0
        assert result["maintenance_rate"] == 25.0
        assert result["availability_rate"] == 50.0

    def test_get_task_completion_stats_empty_list(self):
        """测试空任务列表的统计"""
        result = self.monitor.get_task_completion_stats([])
        assert result == {}

    def test_get_task_completion_stats_normal(self):
        """测试正常任务完成统计"""
        tasks = [
            Task(
                task_id="T1",
                task_type=TaskType.DELIVERY,
                target_position=Position(x=1, y=1),
                status=TaskStatus.PENDING,
            ),
            Task(
                task_id="T2",
                task_type=TaskType.CLEANING,
                target_position=Position(x=2, y=2),
                status=TaskStatus.ASSIGNED,
            ),
            Task(
                task_id="T3",
                task_type=TaskType.DELIVERY,
                target_position=Position(x=3, y=3),
                status=TaskStatus.IN_PROGRESS,
            ),
            Task(
                task_id="T4",
                task_type=TaskType.CLEANING,
                target_position=Position(x=4, y=4),
                status=TaskStatus.COMPLETED,
            ),
            Task(
                task_id="T5",
                task_type=TaskType.DELIVERY,
                target_position=Position(x=5, y=5),
                status=TaskStatus.FAILED,
            ),
        ]

        result = self.monitor.get_task_completion_stats(tasks)

        assert result["total_tasks"] == 5
        assert result["pending_rate"] == 20.0
        assert result["assigned_rate"] == 20.0
        assert result["in_progress_rate"] == 20.0
        assert result["completion_rate"] == 20.0
        assert result["failure_rate"] == 20.0

    def test_get_battery_status_empty_list(self):
        """测试空机器人列表的电池状态"""
        result = self.monitor.get_battery_status([])
        assert result == {}

    def test_get_battery_status_normal(self):
        """测试正常电池状态统计"""
        robots = [
            Robot(
                robot_id="R1",
                name="Robot1",
                position=Position(x=0, y=0),
                battery_level=90,
            ),
            Robot(
                robot_id="R2",
                name="Robot2",
                position=Position(x=1, y=1),
                battery_level=15,
            ),  # 低电量
            Robot(
                robot_id="R3",
                name="Robot3",
                position=Position(x=2, y=2),
                battery_level=5,
            ),  # 极低电量
            Robot(
                robot_id="R4",
                name="Robot4",
                position=Position(x=3, y=3),
                battery_level=50,
            ),
        ]

        result = self.monitor.get_battery_status(robots)

        assert result["average_battery"] == 40.0
        assert result["min_battery"] == 5
        assert result["max_battery"] == 90
        assert result["low_battery_count"] == 2  # 15% 和 5%
        assert result["critical_battery_count"] == 1  # 5%
        assert result["low_battery_rate"] == 50.0

    def test_generate_status_report(self):
        """测试状态报告生成"""
        robots = [Robot(robot_id="R1", name="Robot1", position=Position(x=0, y=0))]
        tasks = [
            Task(
                task_id="T1",
                task_type=TaskType.DELIVERY,
                target_position=Position(x=1, y=1),
            )
        ]

        report = self.monitor.generate_status_report(robots, tasks)

        assert "机器人调度系统状态报告" in report
        assert "机器人状态:" in report
        assert "任务状态:" in report
        assert "电池状态:" in report

    def test_get_system_health_score_no_robots(self):
        """测试无机器人时的健康度评分"""
        score = self.monitor.get_system_health_score([], [])
        assert score == 0.0

    def test_get_system_health_score_normal(self):
        """测试正常系统健康度评分"""
        robots = [
            Robot(
                robot_id="R1",
                name="Robot1",
                position=Position(x=0, y=0),
                battery_level=80,
            ),
            Robot(
                robot_id="R2",
                name="Robot2",
                position=Position(x=1, y=1),
                battery_level=70,
            ),
        ]
        tasks = [
            Task(
                task_id="T1",
                task_type=TaskType.DELIVERY,
                target_position=Position(x=1, y=1),
                status=TaskStatus.COMPLETED,
            ),
        ]

        score = self.monitor.get_system_health_score(robots, tasks)
        assert 0 <= score <= 100

    def test_get_alert_conditions_normal(self):
        """测试正常情况下的告警检查"""
        robots = [
            Robot(
                robot_id="R1",
                name="Robot1",
                position=Position(x=0, y=0),
                battery_level=80,
            )
        ]
        tasks = [
            Task(
                task_id="T1",
                task_type=TaskType.DELIVERY,
                target_position=Position(x=1, y=1),
            )
        ]

        alerts = self.monitor.get_alert_conditions(robots, tasks)
        assert isinstance(alerts, list)

    def test_get_alert_conditions_low_battery(self):
        """测试低电量告警"""
        robots = [
            Robot(
                robot_id="R1",
                name="Robot1",
                position=Position(x=0, y=0),
                battery_level=5,
            ),  # 极低电量
            Robot(
                robot_id="R2",
                name="Robot2",
                position=Position(x=1, y=1),
                battery_level=15,
            ),  # 低电量
        ]

        alerts = self.monitor.get_alert_conditions(robots, [])
        assert len(alerts) > 0
        assert any("电量极低" in alert for alert in alerts)

    def test_get_alert_conditions_high_failure_rate(self):
        """测试高失败率告警"""
        tasks = [
            Task(
                task_id="T1",
                task_type=TaskType.DELIVERY,
                target_position=Position(x=1, y=1),
                status=TaskStatus.FAILED,
            ),
            Task(
                task_id="T2",
                task_type=TaskType.DELIVERY,
                target_position=Position(x=2, y=2),
                status=TaskStatus.FAILED,
            ),
            Task(
                task_id="T3",
                task_type=TaskType.DELIVERY,
                target_position=Position(x=3, y=3),
                status=TaskStatus.COMPLETED,
            ),
        ]
        robots = [Robot(robot_id="R1", name="Robot1", position=Position(x=0, y=0))]

        alerts = self.monitor.get_alert_conditions(robots, tasks)
        assert any("失败率" in alert for alert in alerts)
