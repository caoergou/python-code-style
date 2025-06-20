# GitHub CI 工作流说明

## 概述

这个CI工作流用于验证Python代码的质量，包括代码风格检查、类型检查、单元测试和覆盖率报告。工作流会在每次推送到主分支或创建Pull Request时自动运行。

## 工作流功能

### 1. 代码验证 (validate)

这个作业会在多个Python版本（3.10、3.11、3.12）上运行以下验证步骤：

#### 代码风格检查 (Ruff)

- 检查代码是否符合Google Python代码风格规范
- 检查导入顺序、变量命名、代码复杂度等
- 使用项目中的`pyproject.toml`配置

#### 代码格式化检查 (Ruff Format)

- 检查代码是否已正确格式化
- 确保代码风格一致性

#### 类型检查 (Pyright)

- 检查类型注解的正确性
- 发现潜在的类型错误
- 使用项目中的Pyright配置

#### 单元测试 (Pytest)

- 运行所有测试用例
- 生成测试覆盖率报告
- 确保代码功能正确性

## 输出文件

### 覆盖率报告

- **HTML格式**: 详细的覆盖率报告，包含每个文件的覆盖率信息
- **终端输出**: 在CI日志中显示覆盖率摘要

### 验证报告

- **Markdown格式**: 包含所有验证步骤的结果摘要
- 显示检查时间和Python版本信息

## 如何查看结果

1. **在GitHub Actions页面**:
   - 进入项目的Actions标签页
   - 点击具体的workflow运行记录
   - 查看每个步骤的详细日志

2. **下载报告文件**:
   - 在workflow运行完成后，点击"Artifacts"
   - 下载`coverage-reports-{python-version}`查看HTML覆盖率报告
   - 下载`validation-report-{python-version}`查看验证摘要

## 本地运行

您也可以在本地运行相同的验证命令：

```bash
# 安装依赖
uv sync --group dev

# 代码风格检查
uv run ruff check .

# 格式化检查
uv run ruff format --check .

# 类型检查
uv run pyright src/

# 运行测试和覆盖率
uv run pytest --cov=src --cov-report=html
```

## 故障排除

### 常见问题

1. **代码风格检查失败**:
   - 运行 `uv run ruff check .` 查看具体错误
   - 运行 `uv run ruff format .` 自动修复格式问题

2. **类型检查失败**:
   - 检查类型注解是否正确
   - 查看Pyright的错误信息

3. **测试失败**:
   - 检查测试用例是否正确
   - 确保所有依赖都已安装

### 覆盖率要求

项目设置了80%的最低覆盖率要求。如果覆盖率不足，需要：

- 添加更多测试用例
- 检查是否有不必要的代码
- 考虑排除不需要测试的代码

## 配置说明

工作流使用项目根目录的`pyproject.toml`文件进行配置，包括：

- Ruff的代码风格规则
- Pyright的类型检查设置
- Pytest的测试配置
- Coverage的覆盖率设置

如需修改配置，请编辑`pyproject.toml`文件。
