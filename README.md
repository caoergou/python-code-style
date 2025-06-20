# Python 代码规范与开发流程指南

这个项目展示了如何使用现代Python工具链来维护高质量的代码，包括代码规范检查、自动化测试、持续集成等最佳实践。

## 🎯 项目目标

- 展示现代Python项目的标准开发流程
- 提供完整的代码规范配置和示例
- 演示自动化测试和代码质量保证
- 建立可复用的项目模板

## 🛠️ 技术栈

- **Python 3.10+**: 现代Python特性支持
- **Ruff**: 极速的Python代码检查器和格式化工具
- **Pytest**: 强大的测试框架
- **Pydantic**: 数据验证和设置管理
- **UV**: 快速的Python包管理器
- **MyPy**: 静态类型检查器

## 📁 项目结构

```text
python-code-style/
├── src/                    # 源代码目录
│   ├── models/             # 数据模型定义
│   │   ├── __init__.py
│   │   ├── robot.py        # 机器人模型
│   │   └── task.py         # 任务模型
│   ├── scheduler/          # 业务逻辑层
│   │   ├── __init__.py
│   │   └── robot_scheduler.py
│   ├── services/           # 服务层
│   │   ├── __init__.py
│   │   └── task_service.py
│   ├── utils/              # 工具函数
│   │   ├── __init__.py
│   │   ├── location_utils.py
│   │   ├── status_monitor.py
│   │   └── validators.py
│   └── example.py          # 使用示例
├── tests/                  # 测试代码
│   ├── conftest.py         # 测试配置
│   ├── test_models/        # 模型测试
│   ├── test_scheduler/     # 调度器测试
│   ├── test_services/      # 服务测试
│   └── test_utils/         # 工具测试
├── pyproject.toml          # 项目配置
├── uv.lock                 # 依赖锁定文件
├── README.md               # 项目文档
└── main.py                 # 主程序入口
```

## 🚀 快速开始

### 环境准备

```bash
# 1. 安装uv（如果未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 克隆项目
git clone <repository-url>
cd python-code-style
```

### 安装依赖

```bash
# 安装所有依赖（包括开发依赖）
uv sync
```

### 运行示例

```bash
# 运行主程序
uv run python main.py

# 运行示例代码
uv run python src/example.py
```

## 🔄 标准开发流程

### 1. 代码开发阶段

```bash
# 1. 创建新功能分支
git checkout -b feature/new-feature

# 2. 编写代码时实时检查
uv run ruff check --watch

# 3. 自动格式化代码
uv run ruff format

# 4. 运行测试
uv run pytest

# 5. 检查测试覆盖率
uv run pytest --cov=src --cov-report=html
```

### 2. 代码提交前检查

```bash
# 完整的代码质量检查
uv run ruff check          # 代码风格检查
uv run ruff format --check # 格式化检查
uv run mypy src/           # 类型检查
uv run pytest              # 单元测试
uv run pytest --cov=src    # 覆盖率检查
```

### 3. 持续集成检查

项目配置了以下自动化检查：

- **代码风格**: Ruff linting (E, W, F, I, B, C4, UP, SIM, N, D)
- **代码格式化**: Ruff formatting
- **类型检查**: MyPy 静态类型检查
- **单元测试**: Pytest with coverage

## 📋 详细代码规范

### 1. 导入规范

```python
# 标准库导入
import os
import sys
from typing import List, Optional

# 第三方库导入
import pydantic
from pydantic import BaseModel

# 本地导入
from src.models.robot import Robot
from src.utils.validators import validate_position
```

**规则**:

- 按标准库 → 第三方库 → 本地库的顺序导入
- 每组之间用空行分隔
- 避免使用 `from module import *`
- 相对导入优先于绝对导入

### 2. 文档字符串规范

```python
def calculate_distance(pos1: Position, pos2: Position) -> float:
    """计算两点之间的欧几里得距离

    Args:
        pos1: 第一个位置坐标
        pos2: 第二个位置坐标

    Returns:
        两点之间的距离

    Raises:
        ValueError: 当坐标无效时抛出

    Example:
        >>> pos1 = Position(x=0, y=0)
        >>> pos2 = Position(x=3, y=4)
        >>> calculate_distance(pos1, pos2)
        5.0
    """
    if not pos1.is_valid() or not pos2.is_valid():
        raise ValueError("Invalid position coordinates")

    return ((pos2.x - pos1.x) ** 2 + (pos2.y - pos1.y) ** 2) ** 0.5
```

**规则**:

- 使用Google风格的文档字符串
- 所有公共函数、类、模块必须有文档字符串
- 包含Args、Returns、Raises、Example等部分
- 使用类型注解

### 3. 命名规范

```python
# 变量和函数：snake_case
user_name = "张三"
def get_user_info():
    pass

# 类名：PascalCase
class RobotScheduler:
    pass

# 常量：UPPER_CASE
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30

# 私有成员：_leading_underscore
class Robot:
    def __init__(self):
        self._internal_state = {}

    def _private_method(self):
        pass
```

### 4. 代码长度和格式

```python
# 行长度限制：88字符
def complex_function_with_long_parameters(
    param1: str,
    param2: int,
    param3: List[float],
    param4: Optional[Dict[str, Any]] = None,
) -> Result:
    """复杂函数的示例，展示长参数列表的处理方式"""
    # 复杂表达式适当换行
    result = (
        param1.upper()
        .replace(" ", "_")
        .strip()
    )

    return result
```

### 5. 错误处理

```python
def safe_operation(data: Dict[str, Any]) -> Optional[str]:
    """安全的操作示例，展示异常处理最佳实践"""
    try:
        result = process_data(data)
        return result
    except ValueError as e:
        logger.warning(f"数据验证失败: {e}")
        return None
    except KeyError as e:
        logger.error(f"缺少必要字段: {e}")
        raise
    except Exception as e:
        logger.error(f"未知错误: {e}")
        raise RuntimeError(f"操作失败: {e}") from e
```

## 🧪 测试规范

### 1. 测试文件结构

```python
# tests/test_models/test_robot.py
import pytest
from src.models.robot import Robot, Position

class TestRobot:
    """机器人模型的测试类。"""

    def test_robot_creation(self):
        """测试机器人创建。"""
        robot = Robot(
            robot_id="R001",
            name="测试机器人",
            position=Position(x=0, y=0)
        )
        assert robot.robot_id == "R001"
        assert robot.name == "测试机器人"

    def test_invalid_position(self):
        """测试无效位置的处理。"""
        with pytest.raises(ValueError, match="Invalid position"):
            Robot(
                robot_id="R001",
                name="测试机器人",
                position=Position(x=-1, y=0)
            )
```

### 2. 测试覆盖率要求

- 最低覆盖率：80%
- 核心业务逻辑：90%+
- 工具函数：85%+

## 🔧 工具配置详解

### Ruff 配置说明

```toml
[tool.ruff]
line-length = 88                    # 行长度限制
target-version = "py310"           # Python目标版本

[tool.ruff.lint]
select = [
    "E",   # pycodestyle错误
    "W",   # pycodestyle警告
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "SIM", # flake8-simplify
    "N",   # pep8-naming
    "D",   # pydocstyle
]
```

### 常用命令

```bash
# 代码检查
uv run ruff check                    # 检查所有文件
uv run ruff check src/              # 检查特定目录
uv run ruff check --fix             # 自动修复

# 代码格式化
uv run ruff format                   # 格式化所有文件
uv run ruff format --check          # 检查格式化

# 类型检查
uv run mypy src/                    # 运行类型检查

# 测试
uv run pytest                       # 运行所有测试
uv run pytest -v                    # 详细输出
uv run pytest -k "test_robot"       # 运行特定测试
uv run pytest --cov=src --cov-report=html  # 生成覆盖率报告

```

## 📚 最佳实践

### 1. 代码组织

- **单一职责原则**: 每个模块/类只负责一个功能
- **依赖注入**: 使用依赖注入而不是硬编码依赖
- **配置分离**: 将配置与代码分离
- **错误处理**: 使用适当的异常类型和错误消息

### 2. 性能优化

- 使用类型注解提高代码可读性和IDE支持
- 避免不必要的计算和内存分配
- 使用生成器处理大数据集
- 合理使用缓存装饰器

### 3. 安全性

- 验证所有输入数据
- 使用参数化查询避免SQL注入
- 避免在日志中记录敏感信息
- 使用环境变量管理敏感配置

## 📖 参考资料

- [Ruff 官方文档](https://docs.astral.sh/ruff/)
- [Google Python 风格指南](https://google.github.io/styleguide/pyguide.html)
- [PEP 8 -- Python代码风格指南](https://pep8.org/)
- [Pytest 官方文档](https://docs.pytest.org/)
- [Pydantic 官方文档](https://docs.pydantic.dev/)

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
