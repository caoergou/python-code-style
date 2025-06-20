"""测试位置工具函数"""

import pytest

from src.models.robot import Position, Robot, RobotStatus
from src.utils.location_utils import (
    calculate_center_position,
    calculate_distance,
    calculate_manhattan_distance,
    calculate_travel_time,
    find_nearest_robot,
    find_robots_within_radius,
    is_position_in_bounds,
)


class TestLocationUtils:
    """测试位置工具函数"""

    def test_calculate_distance(self):
        """测试欧几里得距离计算"""
        pos1 = Position(x=0, y=0)
        pos2 = Position(x=3, y=4)

        distance = calculate_distance(pos1, pos2)
        assert distance == 5.0

    def test_calculate_distance_same_position(self):
        """测试相同位置的距离"""
        pos = Position(x=1, y=1)
        distance = calculate_distance(pos, pos)
        assert distance == 0.0

    def test_calculate_manhattan_distance(self):
        """测试曼哈顿距离计算"""
        pos1 = Position(x=0, y=0)
        pos2 = Position(x=3, y=4)

        distance = calculate_manhattan_distance(pos1, pos2)
        assert distance == 7.0

    def test_calculate_manhattan_distance_negative(self):
        """测试负坐标的曼哈顿距离"""
        pos1 = Position(x=-2, y=-3)
        pos2 = Position(x=1, y=2)

        distance = calculate_manhattan_distance(pos1, pos2)
        assert distance == 8.0  # |1-(-2)| + |2-(-3)| = 3 + 5 = 8

    def test_find_nearest_robot_empty_list(self):
        """测试空机器人列表"""
        target = Position(x=0, y=0)
        result = find_nearest_robot(target, [])
        assert result is None

    def test_find_nearest_robot_single_robot(self):
        """测试单个机器人"""
        target = Position(x=0, y=0)
        robot = Robot(robot_id="R1", name="Robot1", position=Position(x=1, y=1))

        result = find_nearest_robot(target, [robot])
        assert result == robot

    def test_find_nearest_robot_multiple_robots(self):
        """测试多个机器人找最近的"""
        target = Position(x=0, y=0)
        robot1 = Robot(robot_id="R1", name="Robot1", position=Position(x=5, y=5))
        robot2 = Robot(
            robot_id="R2", name="Robot2", position=Position(x=1, y=1)
        )  # 更近
        robot3 = Robot(robot_id="R3", name="Robot3", position=Position(x=3, y=3))

        result = find_nearest_robot(target, [robot1, robot2, robot3])
        assert result == robot2

    def test_find_nearest_robot_available_only(self):
        """测试只查找可用机器人"""
        target = Position(x=0, y=0)
        robot1 = Robot(
            robot_id="R1",
            name="Robot1",
            position=Position(x=1, y=1),
            status=RobotStatus.BUSY,
        )
        robot2 = Robot(
            robot_id="R2",
            name="Robot2",
            position=Position(x=2, y=2),
            status=RobotStatus.IDLE,
        )

        # 不限制可用性
        result = find_nearest_robot(target, [robot1, robot2], available_only=False)
        assert result == robot1  # 更近但忙碌

        # 只查找可用的
        result = find_nearest_robot(target, [robot1, robot2], available_only=True)
        assert result == robot2  # 稍远但可用

    def test_find_nearest_robot_no_available(self):
        """测试没有可用机器人的情况"""
        target = Position(x=0, y=0)
        robot = Robot(
            robot_id="R1",
            name="Robot1",
            position=Position(x=1, y=1),
            status=RobotStatus.MAINTENANCE,
        )

        result = find_nearest_robot(target, [robot], available_only=True)
        assert result is None

    def test_find_robots_within_radius_empty_list(self):
        """测试空机器人列表的半径搜索"""
        center = Position(x=0, y=0)
        result = find_robots_within_radius(center, [], 10.0)
        assert result == []

    def test_find_robots_within_radius_normal(self):
        """测试正常半径搜索"""
        center = Position(x=0, y=0)
        robot1 = Robot(
            robot_id="R1", name="Robot1", position=Position(x=1, y=1)
        )  # 距离 √2 ≈ 1.41
        robot2 = Robot(
            robot_id="R2", name="Robot2", position=Position(x=5, y=5)
        )  # 距离 √50 ≈ 7.07
        robot3 = Robot(
            robot_id="R3", name="Robot3", position=Position(x=10, y=10)
        )  # 距离 √200 ≈ 14.14

        result = find_robots_within_radius(center, [robot1, robot2, robot3], 8.0)
        assert len(result) == 2
        assert robot1 in result
        assert robot2 in result
        assert robot3 not in result

    def test_find_robots_within_radius_sorted_by_distance(self):
        """测试半径内机器人按距离排序"""
        center = Position(x=0, y=0)
        robot1 = Robot(
            robot_id="R1", name="Robot1", position=Position(x=3, y=4)
        )  # 距离 5
        robot2 = Robot(
            robot_id="R2", name="Robot2", position=Position(x=1, y=1)
        )  # 距离 √2 ≈ 1.41

        result = find_robots_within_radius(center, [robot1, robot2], 10.0)
        assert result[0] == robot2  # 更近的排在前面
        assert result[1] == robot1

    def test_calculate_center_position_empty_list(self):
        """测试空位置列表的中心计算"""
        result = calculate_center_position([])
        assert result is None

    def test_calculate_center_position_single_position(self):
        """测试单个位置的中心"""
        pos = Position(x=5, y=10)
        result = calculate_center_position([pos])

        assert result is not None
        assert result.x == 5
        assert result.y == 10

    def test_calculate_center_position_multiple_positions(self):
        """测试多个位置的中心计算"""
        positions = [
            Position(x=0, y=0),
            Position(x=4, y=0),
            Position(x=2, y=6),
        ]
        result = calculate_center_position(positions)
        assert result is not None
        assert result.x == 2.0  # (0+4+2)/3
        assert result.y == 2.0  # (0+0+6)/3

    def test_is_position_in_bounds_custom_bounds(self):
        """测试自定义边界检查"""
        pos = Position(x=5, y=5)

        assert is_position_in_bounds(pos, 0, 10, 0, 10) is True
        assert is_position_in_bounds(pos, 0, 4, 0, 10) is False
        assert is_position_in_bounds(pos, 0, 10, 0, 4) is False

    def test_is_position_in_bounds_edge_cases(self):
        """测试边界值情况"""
        # 边界上的点应该被包含
        pos_edge = Position(x=10, y=10)
        assert is_position_in_bounds(pos_edge, 0, 10, 0, 10) is True

    def test_calculate_travel_time_normal(self):
        """测试正常旅行时间计算"""
        distance = 10.0
        speed = 2.0
        time = calculate_travel_time(distance, speed)
        assert time == 5.0

    def test_calculate_travel_time_default_speed(self):
        """测试默认速度的旅行时间"""
        distance = 5.0
        time = calculate_travel_time(distance)
        assert time == 5.0  # 默认速度为1.0

    def test_calculate_travel_time_zero_speed(self):
        """测试零速度抛出异常"""
        with pytest.raises(ValueError, match="速度必须大于0"):
            calculate_travel_time(10.0, 0.0)

    def test_calculate_travel_time_negative_speed(self):
        """测试负速度抛出异常"""
        with pytest.raises(ValueError, match="速度必须大于0"):
            calculate_travel_time(10.0, -1.0)
