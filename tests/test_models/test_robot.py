"""机器人模型测试 - 展示Pydantic模型测试最佳实践。

这个模块测试机器人模型的所有功能，
展示了如何编写高质量的单元测试。
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from src.models.robot import Position, Robot, RobotStatus


class TestPosition:
    """位置模型测试类"""

    def test_create_valid_position(self):
        """测试创建有效位置"""
        pos = Position(x=10.5, y=-5.2)
        assert pos.x == 10.5
        assert pos.y == -5.2

    def test_position_bounds_validation(self):
        """测试位置边界验证"""
        # 测试超出上界
        with pytest.raises(ValidationError) as exc_info:
            Position(x=1001, y=0)
        assert "Input should be less than or equal to 1000" in str(exc_info.value)

        # 测试超出下界
        with pytest.raises(ValidationError) as exc_info:
            Position(x=0, y=-1001)
        assert "Input should be greater than or equal to -1000" in str(exc_info.value)

    def test_position_distance_calculation(self):
        """测试距离计算方法"""
        pos1 = Position(x=0, y=0)
        pos2 = Position(x=3, y=4)

        distance = pos1.distance_to(pos2)
        assert distance == 5.0  # 3-4-5三角形

    def test_position_distance_same_point(self):
        """测试相同点的距离"""
        pos = Position(x=5, y=5)
        distance = pos.distance_to(pos)
        assert distance == 0.0

    def test_position_serialization(self):
        """测试位置序列化"""
        pos = Position(x=10.5, y=-5.2)
        data = pos.model_dump()

        assert data == {"x": 10.5, "y": -5.2}

    def test_position_from_dict(self):
        """测试从字典创建位置"""
        data = {"x": 15.0, "y": -10.5}
        pos = Position(**data)

        assert pos.x == 15.0
        assert pos.y == -10.5


class TestRobot:
    """机器人模型测试类"""

    def test_create_valid_robot(self, sample_position: Position):
        """测试创建有效机器人"""
        robot = Robot(robot_id="R001", name="测试机器人", position=sample_position)

        assert robot.robot_id == "R001"
        assert robot.name == "测试机器人"
        assert robot.position == sample_position
        assert robot.status == RobotStatus.IDLE
        assert robot.battery_level == 100.0
        assert robot.current_task is None
        assert isinstance(robot.created_at, datetime)

    def test_robot_id_validation(self, sample_position: Position):
        """测试机器人ID验证"""
        # 测试无效ID（不以R开头）
        with pytest.raises(ValidationError) as exc_info:
            Robot(robot_id="INVALID", name="测试机器人", position=sample_position)
        assert "机器人ID必须以R开头" in str(exc_info.value)

        # 测试空ID
        with pytest.raises(ValidationError):
            Robot(robot_id="", name="测试机器人", position=sample_position)

    def test_robot_name_validation(self, sample_position: Position):
        """测试机器人名称验证"""
        # 测试空名称
        with pytest.raises(ValidationError) as exc_info:
            Robot(robot_id="R001", name="", position=sample_position)
        assert "机器人名称不能为空" in str(exc_info.value)

        # 测试只有空格的名称
        with pytest.raises(ValidationError):
            Robot(robot_id="R001", name="   ", position=sample_position)

    def test_battery_level_validation(self, sample_position: Position):
        """测试电池电量验证"""
        # 测试负数电量
        with pytest.raises(ValidationError):
            Robot(
                robot_id="R001",
                name="测试机器人",
                position=sample_position,
                battery_level=-1,
            )

        # 测试超过100的电量
        with pytest.raises(ValidationError):
            Robot(
                robot_id="R001",
                name="测试机器人",
                position=sample_position,
                battery_level=101,
            )

    def test_robot_is_available(self, sample_position: Position):
        """测试机器人可用性检查"""
        # 测试正常可用机器人
        robot = Robot(
            robot_id="R001",
            name="测试机器人",
            position=sample_position,
            status=RobotStatus.IDLE,
            battery_level=50,
        )
        assert robot.is_available() is True

        # 测试低电量机器人
        robot.battery_level = 10
        assert robot.is_available() is False

        # 测试忙碌机器人
        robot.battery_level = 80
        robot.status = RobotStatus.BUSY
        assert robot.is_available() is False

        # 测试充电中机器人
        robot.status = RobotStatus.CHARGING
        assert robot.is_available() is False

    def test_robot_assign_task(self, sample_robot: Robot):
        """测试任务分配"""
        # 测试成功分配
        sample_robot.assign_task("T001")
        assert sample_robot.current_task == "T001"
        assert sample_robot.status == RobotStatus.BUSY

        # 测试对不可用机器人分配任务
        with pytest.raises(ValueError) as exc_info:
            sample_robot.assign_task("T002")  # 机器人已经忙碌
        assert "不可用" in str(exc_info.value)

    def test_robot_complete_task(self, sample_robot: Robot):
        """测试任务完成"""
        # 先分配任务
        sample_robot.assign_task("T001")
        assert sample_robot.current_task == "T001"
        assert sample_robot.status == RobotStatus.BUSY

        # 完成任务
        sample_robot.complete_task()
        assert sample_robot.current_task is None
        assert sample_robot.status == RobotStatus.IDLE

    def test_robot_move_to(self, sample_robot: Robot):
        """测试机器人移动"""
        original_position = sample_robot.position
        new_position = Position(x=20, y=30)

        sample_robot.move_to(new_position)
        assert sample_robot.position == new_position
        assert sample_robot.position != original_position

    def test_robot_serialization(self, sample_robot: Robot):
        """测试机器人序列化"""
        data = sample_robot.model_dump()

        assert data["robot_id"] == "R001"
        assert data["name"] == "测试机器人"
        assert "position" in data
        assert data["status"] == "idle"
        assert data["battery_level"] == 100.0

    def test_robot_json_export_import(self, sample_robot: Robot):
        """测试JSON导出和导入"""
        # 导出为JSON
        json_str = sample_robot.model_dump_json()
        assert "R001" in json_str
        assert "测试机器人" in json_str

        # 从JSON导入
        data = sample_robot.model_dump()
        new_robot = Robot(**data)

        assert new_robot.robot_id == sample_robot.robot_id
        assert new_robot.name == sample_robot.name
        assert new_robot.position.x == sample_robot.position.x
        assert new_robot.position.y == sample_robot.position.y

    def test_robot_with_all_statuses(self, sample_position: Position):
        """测试机器人的所有状态"""
        for status in RobotStatus:
            robot = Robot(
                robot_id=f"R{status.value}",
                name=f"机器人{status.value}",
                position=sample_position,
                status=status,
            )
            assert robot.status == status

    def test_robot_edge_cases(self, sample_position: Position):
        """测试边界情况"""
        # 测试最小合法电量
        robot = Robot(
            robot_id="R001",
            name="测试机器人",
            position=sample_position,
            battery_level=0.0,
        )
        assert robot.battery_level == 0.0

        # 测试最大合法电量
        robot = Robot(
            robot_id="R002",
            name="测试机器人",
            position=sample_position,
            battery_level=100.0,
        )
        assert robot.battery_level == 100.0

        # 测试最长名称
        long_name = "A" * 100
        robot = Robot(robot_id="R003", name=long_name, position=sample_position)
        assert robot.name == long_name
