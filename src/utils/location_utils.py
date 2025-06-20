"""位置计算工具函数 - 展示数学计算和算法实现。

这个模块包含了与位置、距离计算相关的工具函数，
展示了如何编写清晰的算法实现。
"""

import math

from src.models.robot import Position, Robot


def calculate_distance(pos1: Position, pos2: Position) -> float:
    """计算两个位置之间的欧几里得距离。

    Args:
        pos1: 第一个位置
        pos2: 第二个位置

    Returns:
        两点间的距离

    Example:
        >>> pos1 = Position(x=0, y=0)
        >>> pos2 = Position(x=3, y=4)
        >>> calculate_distance(pos1, pos2)
        5.0
    """
    dx = pos2.x - pos1.x
    dy = pos2.y - pos1.y
    return math.sqrt(dx * dx + dy * dy)


def calculate_manhattan_distance(pos1: Position, pos2: Position) -> float:
    """计算两个位置之间的曼哈顿距离。

    Args:
        pos1: 第一个位置
        pos2: 第二个位置

    Returns:
        曼哈顿距离

    Example:
        >>> pos1 = Position(x=0, y=0)
        >>> pos2 = Position(x=3, y=4)
        >>> calculate_manhattan_distance(pos1, pos2)
        7.0
    """
    return abs(pos2.x - pos1.x) + abs(pos2.y - pos1.y)


def find_nearest_robot(
    target_position: Position, robots: list[Robot], available_only: bool = True
) -> Robot | None:
    """找到距离目标位置最近的机器人。

    Args:
        target_position: 目标位置
        robots: 机器人列表
        available_only: 是否只考虑可用机器人

    Returns:
        最近的机器人，如果没有符合条件的机器人则返回None
    """
    if not robots:
        return None

    # 过滤机器人
    candidates = robots
    if available_only:
        candidates = [robot for robot in robots if robot.is_available()]

    if not candidates:
        return None

    # 找到最近的机器人
    nearest_robot = None
    min_distance = float("inf")

    for robot in candidates:
        distance = calculate_distance(robot.position, target_position)
        if distance < min_distance:
            min_distance = distance
            nearest_robot = robot

    return nearest_robot


def find_robots_within_radius(
    center: Position, robots: list[Robot], radius: float
) -> list[Robot]:
    """找到指定半径内的所有机器人。

    Args:
        center: 中心位置
        robots: 机器人列表
        radius: 搜索半径

    Returns:
        半径内的机器人列表，按距离排序
    """
    robots_in_radius: list[tuple[Robot, float]] = []

    for robot in robots:
        distance = calculate_distance(center, robot.position)
        if distance <= radius:
            robots_in_radius.append((robot, distance))

    # 按距离排序
    robots_in_radius.sort(key=lambda x: x[1])

    return [robot for robot, _ in robots_in_radius]


def calculate_center_position(positions: list[Position]) -> Position | None:
    """计算位置列表的中心点。

    Args:
        positions: 位置列表

    Returns:
        中心位置，如果列表为空则返回None
    """
    if not positions:
        return None

    total_x = sum(pos.x for pos in positions)
    total_y = sum(pos.y for pos in positions)
    count = len(positions)

    return Position(x=total_x / count, y=total_y / count)


def is_position_in_bounds(
    position: Position,
    min_x: float = -1000,
    max_x: float = 1000,
    min_y: float = -1000,
    max_y: float = 1000,
) -> bool:
    """检查位置是否在指定边界内。

    Args:
        position: 要检查的位置
        min_x: X坐标最小值
        max_x: X坐标最大值
        min_y: Y坐标最小值
        max_y: Y坐标最大值

    Returns:
        如果位置在边界内返回True，否则返回False
    """
    return min_x <= position.x <= max_x and min_y <= position.y <= max_y


def calculate_travel_time(distance: float, speed: float = 1.0) -> float:
    """根据距离和速度计算预估旅行时间。

    Args:
        distance: 距离
        speed: 速度(单位/秒)

    Returns:
        预估时间(秒)

    Raises:
        ValueError: 当速度小于等于0时
    """
    if speed <= 0:
        raise ValueError("速度必须大于0")

    return distance / speed
