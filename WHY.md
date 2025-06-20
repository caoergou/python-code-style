# 工具选型与规则调整指南

本文档详细说明了项目中各个工具的选型原因、配置说明以及如何根据团队需求调整规则。

## 🛠️ 工具选型详解

### 1. UV 包管理器

**选择原因**:

- **速度**: 比 pip 快 10-100 倍，比 Poetry 快 2-3 倍
- **依赖解析**: 使用 Rust 实现，解析速度快且准确
- **虚拟环境**: 自动管理虚拟环境，无需手动创建
- **锁定文件**: 生成精确的依赖锁定文件，确保环境一致性

**替代方案对比**:

- **Poetry**: 功能丰富但速度较慢，配置复杂
- **Pipenv**: 已不再积极维护
- **pip + venv**: 基础功能，但需要手动管理

### 2. Ruff 代码检查器

**选择原因**:

- **性能**: 用 Rust 编写，比传统工具快 10-100 倍
- **功能完整**: 集成了 linting、formatting、import sorting 等功能
- **配置简单**: 单一配置文件，规则丰富
- **活跃维护**: Astral 团队积极维护，更新频繁

**规则集说明**:

```toml
select = [
    "E",   # pycodestyle错误 - 基础代码风格
    "W",   # pycodestyle警告 - 代码风格警告
    "F",   # pyflakes - 逻辑错误检测
    "I",   # isort - 导入排序
    "B",   # flake8-bugbear - 常见错误检测
    "C4",  # flake8-comprehensions - 列表推导式优化
    "UP",  # pyupgrade - 代码现代化
    "SIM", # flake8-simplify - 代码简化
    "N",   # pep8-naming - 命名规范
    "D",   # pydocstyle - 文档字符串规范
]
```

**替代方案对比**:

- **Flake8 + Black + isort**: 功能分散，配置复杂，速度慢
- **Pylint**: 功能强大但速度慢，误报较多
- **PyLama**: 多工具集成，但配置复杂

### 3. Pyright 类型检查器

**选择原因**:

- **性能**: 微软开发，性能优秀
- **准确性**: 错误检测准确，误报率低
- **IDE集成**: 与 VS Code 完美集成
- **配置灵活**: 支持多种检查模式

**检查模式**:

- **off**: 关闭类型检查
- **basic**: 基础检查（推荐）
- **strict**: 严格检查

**替代方案对比**:

- **MyPy**: 功能强大但速度较慢，配置复杂
- **Pyre**: Facebook 开发，但社区相对较小

### 4. Pytest 测试框架

**选择原因**:

- **功能强大**: 支持参数化、fixture、插件等
- **社区活跃**: 插件丰富，文档完善
- **配置简单**: 开箱即用，配置灵活
- **报告丰富**: 支持多种报告格式

## 🔧 Ruff 规则调整指南

### 查看所有可用规则

```bash
# 查看所有规则
uv run ruff rule --all

# 查看特定规则详情
uv run ruff rule E501

# 查看规则分类
uv run ruff rule --select E
```

### 规则调整方法

#### 1. 忽略特定规则

如果某个规则不适合项目需求：

```toml
[tool.ruff.lint]
ignore = [
    "E501",  # 行长度限制
    "D100",  # 缺少模块文档字符串
    "D104",  # 缺少公共包文档字符串
    "T201",  # 打印语句
    "UP007", # 使用 X | Y 而不是 Union[X, Y]
]
```

#### 2. 忽略特定文件或目录

```toml
[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401", "D104"]  # 忽略未使用的导入和缺少文档字符串
"tests/*" = ["D100", "D103", "D104"]  # 测试文件忽略文档字符串要求
"src/legacy/*" = ["E501", "W503"]  # 遗留代码忽略某些规则
```

#### 3. 调整规则参数

```toml
# 调整行长度限制
[tool.ruff.lint.pycodestyle]
max-line-length = 100

# 调整文档字符串风格
[tool.ruff.lint.pydocstyle]
convention = "google"  # 可选: "google", "pep257", "numpy"

# 调整导入排序
[tool.ruff.lint.isort]
known-first-party = ["src"]
known-third-party = ["pydantic", "pytest"]
```

#### 4. 自定义规则配置

```toml
# 配置特定规则的参数
[tool.ruff.lint.pycodestyle]
max-line-length = 88
ignore-long-lines = ["E501"]

[tool.ruff.lint.pydocstyle]
convention = "google"
ignore-decorators = ["property", "classmethod", "staticmethod"]
```

### 规则调整建议流程

#### 1. 收集反馈阶段

- **问题识别**: 团队成员发现某个规则不合理
- **影响评估**: 分析规则对开发效率的影响
- **替代方案**: 考虑是否有更好的解决方案

#### 2. 讨论决策阶段

- **团队讨论**: 在团队会议中讨论调整建议
- **利弊分析**: 权衡调整的利弊
- **投票决策**: 团队投票决定是否调整

#### 3. 实施验证阶段

- **配置调整**: 在测试分支中调整配置
- **效果验证**: 运行完整检查验证效果
- **文档更新**: 更新相关文档

#### 4. 推广应用阶段

- **团队通知**: 通知所有团队成员
- **培训说明**: 解释调整原因和影响
- **监控反馈**: 收集使用反馈

### 常见规则调整场景

#### 1. 行长度限制 (E501)

**场景**: 团队习惯使用更长的行长度

**调整方法**:

```toml
[tool.ruff.lint.pycodestyle]
max-line-length = 120
```

**考虑因素**:

- 显示器分辨率
- 代码可读性
- 团队习惯

#### 2. 文档字符串要求 (D系列规则)

**场景**: 某些文件不需要完整的文档字符串

**调整方法**:

```toml
[tool.ruff.lint]
ignore = ["D100", "D104"]  # 忽略模块和包文档字符串要求

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["D100", "D103", "D104"]  # 测试文件忽略文档字符串
"__init__.py" = ["D104"]  # 初始化文件忽略包文档字符串
```

#### 3. 导入排序 (I系列规则)

**场景**: 需要自定义导入分组

**调整方法**:

```toml
[tool.ruff.lint.isort]
known-first-party = ["src"]
known-third-party = ["pydantic", "pytest", "requests"]
section-order = ["future", "standard-library", "third-party", "first-party", "local-folder"]
```

#### 4. 命名规范 (N系列规则)

**场景**: 需要调整变量命名规则

**调整方法**:

```toml
[tool.ruff.lint.pep8-naming]
classmethod-decorators = ["classmethod", "validator"]
```

## 🚀 团队协作最佳实践

### 1. 规则调整原则

- **一致性**: 保持团队代码风格一致
- **可读性**: 优先考虑代码可读性
- **效率**: 平衡代码质量与开发效率
- **维护性**: 考虑长期维护成本

### 2. 沟通建议

- **及时反馈**: 发现问题及时提出
- **建设性**: 提供建设性的改进建议
- **文档化**: 重要决策要文档化
- **定期回顾**: 定期回顾和优化规则

### 3. 培训与推广

- **新成员培训**: 新成员加入时进行规范培训
- **定期分享**: 定期分享最佳实践
- **工具使用**: 培训团队成员正确使用工具
- **问题解答**: 建立问题解答机制

### 4. 持续改进

- **收集反馈**: 定期收集团队反馈
- **评估效果**: 评估当前规则的效果
- **优化调整**: 根据反馈优化调整
- **版本管理**: 记录规则变更历史

## 📚 参考资料

### Ruff 相关

- [Ruff 官方文档](https://docs.astral.sh/ruff/)
- [Ruff 规则参考](https://docs.astral.sh/ruff/rules/)
- [Ruff 配置指南](https://docs.astral.sh/ruff/configuration/)
- [Ruff 规则分类](https://docs.astral.sh/ruff/rules/#rule-codes)

### 代码规范

- [Google Python 风格指南](https://google.github.io/styleguide/pyguide.html)
- [PEP 8 -- Python代码风格指南](https://pep8.org/)
- [PEP 257 -- 文档字符串约定](https://peps.python.org/pep-0257/)

### 工具对比

- [Python 包管理器对比](https://packaging.python.org/guides/tool-recommendations/)
- [Python 代码检查工具对比](https://realpython.com/python-code-quality/)
- [Python 类型检查器对比](https://realpython.com/python-type-checking/)

---

**注意**: 本文档会随着工具更新和团队需求变化而持续更新。如有疑问或建议，请通过 Issue 或 Pull Request 参与讨论。
