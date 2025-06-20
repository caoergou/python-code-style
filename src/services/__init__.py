"""服务层包 - 业务逻辑服务。

这个包包含了机器人调度系统的业务服务层，
展示了如何设计清晰的服务架构。
"""

from .task_service import TaskService

__all__ = [
    "TaskService",
]
