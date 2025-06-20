# Python 协作开发代码规范建议

这个项目展示了现代Python团队协作开发的最佳实践，包括代码规范建议、自动化工具配置、测试策略等。本文档旨在为团队提供参考标准，而非强制要求。

## 🎯 项目目标

- 建立团队协作的Python开发标准
- 提供可配置的代码质量工具链
- 展示自动化测试和代码审查流程
- 创建可复用的项目模板和配置

## 🛠️ 技术栈选型与建议

### 核心工具选择

| 工具 | 选择 | 原因 | 替代方案 |
|------|------|------|----------|
| **包管理器** | UV | 极速安装、依赖解析快、支持虚拟环境管理 | Poetry, Pipenv |
| **代码检查** | Ruff | 速度极快、规则丰富、配置简单 | Flake8 + Black + isort |
| **类型检查** | Pyright | 微软开发、性能优秀、错误提示准确 | MyPy |
| **测试框架** | Pytest | 功能强大、插件丰富、社区活跃 | unittest, nose2 |
| **数据验证** | Pydantic | 类型安全、性能优秀、生态完善 | Marshmallow, dataclasses |

### 工具选型考虑因素

1. **性能优先**: Ruff 比传统工具快 10-100 倍
2. **开发体验**: 配置简单，错误提示清晰
3. **社区支持**: 活跃的维护和更新
4. **团队学习成本**: 选择主流工具降低学习成本

> **注意**: 如果团队对某些工具不熟悉，建议先在小范围试用，收集反馈后再决定是否推广。

## 📁 当前项目结构

```text
python-code-style/
├── src/                    # 源代码目录
│   ├── models/             # 数据模型定义
│   ├── scheduler/          # 业务逻辑层
│   ├── services/           # 服务层
│   ├── utils/              # 工具函数
│   └── example.py          # 使用示例
├── tests/                  # 测试代码
├── pyproject.toml          # 项目配置
├── uv.lock                 # 依赖锁定文件
└── README.md               # 项目文档
```

**建议**: 根据项目规模和团队习惯调整目录结构，保持简洁明了。

## 🚀 快速开始

### 环境准备

```bash
# 1. 安装uv（推荐）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 克隆项目
git clone <repository-url>
cd python-code-style
```

### 安装依赖

```bash
# 安装所有依赖
uv sync
```

### 运行示例

```bash
# 运行主程序
uv run python main.py

# 运行示例代码
uv run python src/example.py
```

## 🔄 协作开发流程建议

### 1. 功能开发阶段

#### 创建功能分支

```bash
git checkout -b feature/new-feature
```

#### 依赖管理

```bash
# 添加新依赖
uv add <package-name>

# 添加开发依赖
uv add --dev <package-name>

# 移除依赖
uv remove <package-name>
```

> **建议**:
>
> 1. 定期审查依赖，移除不再使用的包，保持依赖列表简洁
> 2. 对于外部依赖，使用 uv 来管理, 不建议直接修改 pyproject.toml 或 uv.lock 文件
>

#### 实时代码检查

```bash
# 实时检查代码（推荐在开发时使用）
uv run ruff check --watch

# 或者使用编辑器插件
# VS Code: Python + Ruff 插件
# PyCharm: Ruff 插件
```

#### 代码格式化

```bash
# 自动格式化
uv run ruff format

# 检查格式化状态
uv run ruff format --check
```

#### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试
uv run pytest tests/test_models/

# 生成覆盖率报告
uv run pytest --cov=src --cov-report=html
```

### 2. 代码提交前检查

```bash
# 完整的代码质量检查
uv run ruff check          # 代码风格检查
uv run ruff format --check # 格式化检查
uv run pyright src/        # 类型检查
uv run pytest              # 单元测试
uv run pytest --cov=src    # 覆盖率检查
```

> **建议**: 可以配置 Git hooks 自动运行这些检查，确保代码质量。

### 3. 代码审查流程

1. **自检**: 提交前运行完整的代码质量检查
2. **同行评审**: 至少一名团队成员审查代码
3. **自动化检查**: CI/CD 流水线验证代码质量
4. **合并**: 通过所有检查后合并到主分支

## 📋 代码规范建议

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

**建议**:

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

**建议**:

- 使用Google风格的文档字符串
- 所有公共函数、类、模块建议添加文档字符串
- 包含Args、Returns、Raises、Example等部分
- 使用类型注解提高代码可读性

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
# 行长度建议：88字符（可配置）
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

## 🧪 测试规范建议

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

### 2. 测试覆盖率建议

- **最低覆盖率**: 80%（可根据项目复杂度调整）
- **核心业务逻辑**: 90%+
- **工具函数**: 85%+

> **注意**: 覆盖率不是唯一标准，测试质量和业务价值更重要。

## 🔧 工具配置与调整

### Ruff 规则配置

当前配置的规则集：

```toml
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

### 如何调整 Ruff 规则

如果某些规则不适合项目需求，可以通过以下方式调整：

#### 1. 忽略特定规则

```toml
[tool.ruff.lint]
ignore = [
    "E501",  # 行长度限制
    "D100",  # 缺少模块文档字符串
    "D104",  # 缺少公共包文档字符串
]
```

#### 2. 忽略特定文件

```toml
[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401", "D104"]
"tests/*" = ["D100", "D103", "D104"]
```

#### 3. 调整规则参数

```toml
[tool.ruff.lint.pycodestyle]
max-line-length = 100  # 调整行长度限制

[tool.ruff.lint.pydocstyle]
convention = "google"  # 使用Google风格的文档字符串
```

### 规则调整建议流程

1. **收集反馈**: 团队成员提出规则调整需求
2. **讨论影响**: 评估调整对代码质量的影响
3. **测试验证**: 在测试分支中验证调整效果
4. **团队决策**: 团队讨论并决定是否采用
5. **文档更新**: 更新配置和文档

### 常用命令参考

```bash
# 代码检查
uv run ruff check                    # 检查所有文件
uv run ruff check src/              # 检查特定目录
uv run ruff check --fix             # 自动修复

# 代码格式化
uv run ruff format                   # 格式化所有文件
uv run ruff format --check          # 检查格式化

# 类型检查
uv run pyright src/                 # 使用Pyright

# 测试
uv run pytest                       # 运行所有测试
uv run pytest -v                    # 详细输出
uv run pytest -k "test_robot"       # 运行特定测试
uv run pytest --cov=src --cov-report=html  # 生成覆盖率报告
```

## 📚 最佳实践建议

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

## 🤝 团队协作建议

### 1. 代码审查要点

- **功能正确性**: 代码是否实现了预期功能
- **代码质量**: 是否符合项目规范
- **可维护性**: 代码是否易于理解和维护
- **性能影响**: 是否对系统性能有负面影响
- **安全性**: 是否存在安全风险

### 2. 沟通建议

- 使用清晰的提交信息
- 在PR中详细说明变更原因
- 及时响应审查意见
- 保持开放和建设性的讨论氛围

### 3. 知识分享

- 定期进行代码规范培训
- 分享最佳实践和经验教训
- 建立团队知识库
- 鼓励结对编程

## 📖 参考资料

- [Ruff 官方文档](https://docs.astral.sh/ruff/)
- [Ruff 规则参考](https://docs.astral.sh/ruff/rules/)
- [Google Python 风格指南](https://google.github.io/styleguide/pyguide.html)
- [PEP 8 -- Python代码风格指南](https://pep8.org/)
- [Pytest 官方文档](https://docs.pytest.org/)
- [Pydantic 官方文档](https://docs.pydantic.dev/)

> **详细指南**: 查看 [WHY.md](WHY.md) 了解工具选型原因、规则调整方法和团队协作最佳实践。

## 🚀 贡献指南

### 1. 提出改进建议

如果您对代码规范有改进建议：

1. **创建 Issue**: 在项目中创建 Issue 描述建议
2. **提供理由**: 说明为什么需要这个改进
3. **讨论影响**: 分析对团队和项目的影响
4. **等待反馈**: 等待团队讨论和决策

### 2. 提交代码变更

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 3. 参与讨论

- 积极参与代码审查
- 提供建设性的反馈
- 分享经验和最佳实践
- 帮助新团队成员

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**注意**: 本文档中的规范和建议旨在提高团队协作效率，具体实施时可根据项目需求和团队习惯进行调整。如有疑问或建议，欢迎通过 Issue 或 Pull Request 参与讨论。
