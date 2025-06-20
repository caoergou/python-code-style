"""任务模型，使用Pydantic进行数据验证。

这个模块定义了机器人调度系统中的任务实体，
展示了复杂业务对象的建模方式。
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.models.robot import Position


class TaskType(str, Enum):
    """任务类型枚举。

    定义系统支持的任务类型。
    """

    DELIVERY = "delivery"
    PATROL = "patrol"
    CLEANING = "cleaning"


class TaskStatus(str, Enum):
    """任务状态枚举。

    定义任务的生命周期状态。
    """

    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    """任务实体模型。

    表示系统中的一个任务，包含任务信息、执行状态和分配信息。

    Attributes:
        task_id: 任务唯一标识符，必须以'T'开头
        task_type: 任务类型
        target_position: 任务执行的目标位置
        priority: 任务优先级(1-5)，数字越大优先级越高
        status: 任务当前状态
        assigned_robot: 分配执行此任务的机器人ID
        created_at: 任务创建时间
        estimated_duration: 预估执行时间(分钟)
        description: 任务描述信息
    """

    model_config = ConfigDict(str_strip_whitespace=True, use_enum_values=True)

    task_id: str = Field(..., min_length=1, max_length=50, description="任务ID")
    task_type: TaskType = Field(..., description="任务类型")
    target_position: Position = Field(..., description="目标位置")
    priority: int = Field(default=1, ge=1, le=5, description="优先级(1-5)")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="任务状态")
    assigned_robot: str | None = Field(default=None, description="分配的机器人ID")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    estimated_duration: int = Field(
        default=30, ge=1, le=1440, description="预估执行时间(分钟)"
    )
    description: str | None = Field(default="", max_length=500, description="任务描述")

    @field_validator("task_id")
    @classmethod
    def validate_task_id(cls, v: str) -> str:
        """验证任务ID格式。

        Args:
            v: 任务ID

        Returns:
            验证后的任务ID

        Raises:
            ValueError: 当ID格式不正确时
        """
        if not v.startswith("T"):
            raise ValueError("任务ID必须以T开头")
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str | None) -> str:
        """验证任务描述。

        Args:
            v: 任务描述

        Returns:
            验证后的任务描述
        """
        return v.strip() if v else ""

    def is_high_priority(self) -> bool:
        """检查是否为高优先级任务。

        Returns:
            优先级大于等于4时返回True
        """
        return self.priority >= 4

    def is_pending(self) -> bool:
        """检查任务是否为待分配状态。

        Returns:
            状态为PENDING时返回True
        """
        return self.status == TaskStatus.PENDING

    def is_completed(self) -> bool:
        """检查任务是否已完成。

        Returns:
            状态为COMPLETED时返回True
        """
        return self.status == TaskStatus.COMPLETED

    def assign_to_robot(self, robot_id: str) -> None:
        """将任务分配给指定机器人。

        Args:
            robot_id: 机器人ID

        Raises:
            ValueError: 当任务状态不允许分配时
        """
        if not self.is_pending():
            raise ValueError(f"任务{self.task_id}状态为{self.status}，无法分配")

        self.assigned_robot = robot_id
        self.status = TaskStatus.ASSIGNED

    def start_execution(self) -> None:
        """开始执行任务。

        Raises:
            ValueError: 当任务状态不允许开始执行时
        """
        if self.status != TaskStatus.ASSIGNED:
            raise ValueError(f"任务{self.task_id}状态为{self.status}，无法开始执行")

        self.status = TaskStatus.IN_PROGRESS

    def complete(self) -> None:
        """完成任务。

        Raises:
            ValueError: 当任务状态不允许完成时
        """
        if self.status != TaskStatus.IN_PROGRESS:
            raise ValueError(f"任务{self.task_id}状态为{self.status}，无法完成")

        self.status = TaskStatus.COMPLETED

    def fail(self, reason: str = "") -> None:
        """标记任务失败。

        Args:
            reason: 失败原因
        """
        self.status = TaskStatus.FAILED
        if reason:
            self.description = f"{self.description}\n失败原因: {reason}".strip()
