"""验证器工具测试 - 展示工具函数测试

这个模块测试验证器的所有功能，
包括ID验证、位置验证等工具函数。
"""

from src.models.robot import Position
from src.utils.validators import (
    validate_battery_level,
    validate_position,
    validate_robot_id,
    validate_task_id,
)


class TestValidators:
    """验证器测试类"""

    def test_validate_robot_id_valid(self):
        """测试有效机器人ID验证"""
        valid_ids = ["R001", "R123", "R999", "ROBOT001"]

        for robot_id in valid_ids:
            assert validate_robot_id(robot_id) is True

    def test_validate_robot_id_invalid(self):
        """测试无效机器人ID验证"""
        invalid_ids = ["", "001", "A001", "robot001", "r001", "R"]

        for robot_id in invalid_ids:
            assert validate_robot_id(robot_id) is False

    def test_validate_task_id_valid(self):
        """测试有效任务ID验证"""
        valid_ids = ["T001", "T123", "T999", "TASK001"]

        for task_id in valid_ids:
            assert validate_task_id(task_id) is True

    def test_validate_task_id_invalid(self):
        """测试无效任务ID验证"""
        invalid_ids = ["", "001", "A001", "task001", "t001", "T"]

        for task_id in invalid_ids:
            assert validate_task_id(task_id) is False

    def test_validate_battery_level_valid(self):
        """测试有效电池电量验证"""
        valid_levels = [0.0, 25.5, 50.0, 75.5, 100.0]

        for level in valid_levels:
            assert validate_battery_level(level) is True

    def test_validate_battery_level_invalid(self):
        """测试无效电池电量验证"""
        invalid_levels = [-1.0, -0.1, 100.1, 150.0, 200.0]

        for level in invalid_levels:
            assert validate_battery_level(level) is False

    def test_validate_position_valid(self):
        """测试有效位置验证"""
        valid_positions = [
            Position(x=0, y=0),
            Position(x=500, y=-500),
            Position(x=-1000, y=1000),
            Position(x=999.9, y=-999.9),
        ]

        for position in valid_positions:
            assert validate_position(position) is True

    def test_validate_position_invalid(self):
        """测试无效位置验证"""
        # 由于Position使用Pydantic验证，无法创建无效的Position对象
        # 所以我们测试validate_position对非Position对象的处理
        invalid_inputs = [  # type: ignore
            "not a position",
            {"x": 1001, "y": 0},
            None,
            123,
            [1001, 0],
        ]

        for invalid_input in invalid_inputs:  # type: ignore
            assert validate_position(invalid_input) is False

    def test_validate_edge_cases(self):
        """测试边界情况"""
        edge_positions = [
            Position(x=1000, y=1000),
            Position(x=-1000, y=-1000),
            Position(x=1000, y=-1000),
            Position(x=-1000, y=1000),
        ]

        for position in edge_positions:
            assert validate_position(position) is True

        edge_levels = [0.0, 100.0]
        for level in edge_levels:
            assert validate_battery_level(level) is True

    def test_validator_return_values(self):
        """测试验证器返回值"""
        assert validate_robot_id("INVALID") is False
        assert validate_robot_id("R001") is True
        assert validate_task_id("INVALID") is False
        assert validate_task_id("T001") is True
        assert validate_battery_level(-1) is False
        assert validate_battery_level(101) is False
        assert validate_battery_level(50) is True
        assert validate_position("not a position") is False
        assert validate_position(Position(x=500, y=500)) is True

    def test_validator_type_handling(self):
        """测试验证器对不同类型输入的处理"""
        # 测试非字符串输入
        assert validate_robot_id(123) is False
        assert validate_robot_id(None) is False
        assert validate_task_id(123) is False
        assert validate_task_id(None) is False

        # 测试非数字输入
        assert validate_battery_level("50") is False
        assert validate_battery_level(None) is False

        # 测试非Position对象输入
        assert validate_position("not a position") is False
        assert validate_position(None) is False
        assert validate_position({"x": 0, "y": 0}) is False
