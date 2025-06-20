"""数据验证工具函数 - 展示数据验证和错误处理。

这个模块包含了各种数据验证函数，
展示了如何实现健壮的数据验证逻辑。
"""

from typing import Any

from models.robot import Position


def validate_position(position: Any) -> bool:
    """验证位置对象是否有效。

    Args:
        position: 要验证的位置对象

    Returns:
        验证通过返回True，否则返回False
    """
    if not isinstance(position, Position):
        return False

    try:
        # 检查坐标是否在合理范围内
        if not (-1000 <= position.x <= 1000):
            return False
        return -1000 <= position.y <= 1000
    except (AttributeError, TypeError):
        return False


def validate_priority(priority: Any) -> bool:
    """验证优先级值是否有效。

    Args:
        priority: 要验证的优先级值

    Returns:
        验证通过返回True，否则返回False
    """
    if not isinstance(priority, int):
        return False

    return 1 <= priority <= 5


def validate_battery_level(battery_level: Any) -> bool:
    """验证电池电量值是否有效。

    Args:
        battery_level: 要验证的电池电量值

    Returns:
        验证通过返回True，否则返回False
    """
    if not isinstance(battery_level, int | float):
        return False

    return 0 <= battery_level <= 100


def validate_robot_id(robot_id: Any) -> bool:
    """验证机器人ID格式是否正确。

    Args:
        robot_id: 要验证的机器人ID

    Returns:
        验证通过返回True，否则返回False
    """
    if not isinstance(robot_id, str):
        return False

    return robot_id.startswith("R") and 2 <= len(robot_id) <= 50


def validate_task_id(task_id: Any) -> bool:
    """验证任务ID格式是否正确。

    Args:
        task_id: 要验证的任务ID

    Returns:
        验证通过返回True，否则返回False
    """
    if not isinstance(task_id, str):
        return False

    return task_id.startswith("T") and 2 <= len(task_id) <= 50


def validate_name(name: Any) -> bool:
    """验证名称是否有效。

    Args:
        name: 要验证的名称

    Returns:
        验证通过返回True，否则返回False
    """
    return isinstance(name, str) and len(name.strip()) <= 100


def validate_description(description: Any) -> bool:
    """验证描述文本是否有效。

    Args:
        description: 要验证的描述文本

    Returns:
        验证通过返回True，否则返回False
    """
    if description is None:
        return True

    if not isinstance(description, str):
        return False

    return len(description) <= 500


def validate_estimated_duration(duration: Any) -> bool:
    """验证预估时长是否有效。

    Args:
        duration: 要验证的时长（分钟）

    Returns:
        验证通过返回True，否则返回False
    """
    if not isinstance(duration, int):
        return False

    return 1 <= duration <= 1440  # 1分钟到24小时


def sanitize_string(value: str, max_length: int = 100) -> str:
    """清理和规范化字符串。

    Args:
        value: 要清理的字符串
        max_length: 最大长度

    Returns:
        清理后的字符串
    """
    cleaned = value.strip()
    # 限制长度
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]

    return cleaned


def validate_coordinates(x: Any, y: Any) -> bool:
    """验证坐标值是否有效。

    Args:
        x: X坐标
        y: Y坐标

    Returns:
        验证通过返回True，否则返回False
    """
    return (
        isinstance(x, int | float)
        and isinstance(y, int | float)
        and -1000 <= x <= 1000
        and -1000 <= y <= 1000
    )
