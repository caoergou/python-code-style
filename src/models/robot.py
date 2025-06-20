"""机器人实体模型，使用Pydantic进行数据验证。

这个模块展示了如何使用Pydantic来创建类型安全的数据模型，
包含数据验证、序列化和文档生成功能。
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RobotStatus(str, Enum):
    """机器人状态枚举。

    使用字符串枚举以便于序列化和数据库存储。
    """

    IDLE = "idle"
    BUSY = "busy"
    CHARGING = "charging"
    MAINTENANCE = "maintenance"


class Position(BaseModel):
    """位置坐标模型。

    用于表示机器人的位置坐标，包含边界验证。

    Attributes:
        x: X坐标值，范围在-1000到1000之间
        y: Y坐标值，范围在-1000到1000之间
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    x: float = Field(..., ge=-1000, le=1000, description="X坐标")
    y: float = Field(..., ge=-1000, le=1000, description="Y坐标")

    def distance_to(self, other: "Position") -> float:
        """计算到另一个位置的距离。

        Args:
            other: 目标位置

        Returns:
            欧几里得距离
        """
        return float(((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5)


class Robot(BaseModel):
    """机器人实体模型。

    表示系统中的一个机器人实体，包含位置、状态、任务等信息。

    Attributes:
        robot_id: 机器人唯一标识符，必须以'R'开头
        name: 机器人名称
        position: 当前位置坐标
        status: 当前状态，默认为IDLE
        current_task: 当前执行的任务ID
        battery_level: 电池电量百分比(0-100)
        created_at: 创建时间
    """

    robot_id: str = Field(..., description="机器人ID")
    name: str = Field(..., min_length=1, max_length=100, description="机器人名称")
    position: Position = Field(..., description="当前位置")
    status: RobotStatus = Field(default=RobotStatus.IDLE, description="当前状态")
    current_task: str | None = Field(default=None, description="当前执行的任务ID")
    battery_level: float = Field(
        default=100.0, ge=0, le=100, description="电池电量百分比"
    )
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")

    model_config = ConfigDict(str_strip_whitespace=True, use_enum_values=True)

    @field_validator("robot_id")
    @classmethod
    def validate_robot_id(cls, v: str) -> str:
        """验证机器人ID格式。

        Args:
            v: 机器人ID

        Returns:
            验证后的机器人ID

        Raises:
            ValueError: 当ID格式不正确时
        """
        if not v.startswith("R"):
            raise ValueError("机器人ID必须以R开头")
        return v

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """验证机器人名称。

        Args:
            v: 机器人名称

        Returns:
            验证后的机器人名称

        Raises:
            ValueError: 当名称格式不正确时
        """
        if not v.strip():
            raise ValueError("机器人名称不能为空")
        return v.strip()

    def is_available(self) -> bool:
        """检查机器人是否可用于分配任务。

        Returns:
            如果机器人状态为IDLE且电量充足则返回True
        """
        return self.status == RobotStatus.IDLE and self.battery_level > 20

    def assign_task(self, task_id: str) -> None:
        """分配任务给机器人。

        Args:
            task_id: 任务ID

        Raises:
            ValueError: 当机器人不可用时
        """
        if not self.is_available():
            raise ValueError(f"机器人{self.robot_id}不可用")

        self.current_task = task_id
        self.status = RobotStatus.BUSY

    def complete_task(self) -> None:
        """完成当前任务"""
        self.current_task = None
        self.status = RobotStatus.IDLE

    def move_to(self, new_position: Position) -> None:
        """移动机器人到新位置。

        Args:
            new_position: 目标位置
        """
        self.position = new_position
