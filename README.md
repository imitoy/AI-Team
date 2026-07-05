# AI Team - 基于Lua的AI团队协作系统

## 项目介绍

AI Team 是一个基于 luapython 开发的AI团队协作系统，通过模拟软件开发团队中的不同角色（项目经理、系统架构师、开发队长、开发工程师、文档编写员、代码审查员），实现自动化的项目开发流程。系统使用DeepSeek API作为AI引擎，支持工具调用和团队协作。

### 背景及需求
在 AI 浪潮下，AI 编程成了新的趋势，但如何使用 AI 编程便成了新的问题：如何让 AI 语言模型认知了解现有项目？如何让 AI 语言模型对项目进行精准地更改？现有 AI 大模型存在着诸多不足之处，如上下文长度限制、过长上下文会分散注意力等，要解决 AI 编程的问题，就要先解决这些不足之处。

### 设计思路
本项目的主要功能参考人类协作实现。在人工编程的分工合作中，每个人的“上下文”也不需要很长——例如经理只需要知道这些项目在做什么，需要几天完成，开发工程师只需要知道每个人实现对应的哪些模块。

技术上分别对各模块进行封装和拼接：API 调用、角色管理、模型管理、对话管理，这给了这个项目极大的灵活性与可扩展性。凭借着这些特性，后续迭代的稳定性应该会有极大提升。

### 可行性与价值
本项目目前只具有**一些**可行性。这是不可避免的，因为项目必须建立在大量的实验之上，尤其是提示词部分。另外 AI 语言模型输出速度的限制可能会限制实验速度。

本项目目前是一个**探索**式的项目：它旨在探索 AI 多角色协作项目的可行性。目前的实验数据比较乐观：AI 会自动根据自己的职责互相“调用”，从而达到协作目的。

### 目标与未来规划
本项目的目标是成为**一个多 AI 协作进行项目的管理工具**：不仅仅是程序项目，其它项目，未来可能还会使用机器人与现实交互。

项目规划即使用程序设计作为跳板，逐步完成对多 AI 协作的探索。

## 安装与使用
### 操作系统
- 支持的操作系统：Linux

- 可行但未测试的操作系统：MacOS、BSD、HarmoryOS Next。

- 不支持的操作系统：Windows

### 依赖安装
- 运行环境：lua5.4、python3.14，luarocks （其它版本未经测试）

- 项目依赖：luapython、lua-cjson、python-openai。

依赖安装步骤（以 Arch Linux 为例）：

```bash
sudo pacman -Syu
sudo pacman -S lua5.4 luarocks python python-openai
sudo luarocks install luapython --lua-version 5.4
sudo luarocks install lua-cjson --lua-version 5.4
```

### 运行
首先创建一个 DeepSeek API Key 并设置环境变量 `DEEPSEEK_APIKEY` 为你的 API Key：
```bash
export DEEPSEEK_APIKEY=<Your api key>
```

切换到本项目目录下，新建一个文件作为项目文件夹后运行主程序：
```bash
cd AI-Team
mkdir work
cd work
lua5.4 ../main.lua
```

随后在输入框中描述项目（如“制作一个贪吃蛇应用”）。

### 更多角色与其它模型
角色、模型分别在 avatar.lua、models.lua 中设置，详见下文。

## 系统架构

### 主要组件

1. **main.lua** - 程序入口点
2. **communication/** - 核心通信模块
   - `communication.lua` - 通信管理器，处理角色间对话
   - `models.lua` - AI模型配置（目前支持DeepSeek）
   - `avatar.lua` - 角色定义和配置
   - `api.lua` - API接口封装（支持OpenAI兼容API）

### 角色定义

系统包含以下6个角色，每个角色都有明确的职责：

1. **项目经理 (Project Manager)**
   - 理解用户需求并分解为具体任务
   - 分配任务给合适的团队成员
   - 跟踪项目进度并协调团队协作

2. **系统架构师 (System Architect)**
   - 设计系统整体架构和组件交互
   - 确保架构的可扩展性、可维护性和性能
   - 与项目经理和其他团队成员协作

3. **开发队长 (Development Lead)**
   - 接收架构师指派的任务
   - 将任务拆分为小的文件任务
   - 指派给开发工程师并跟踪进度

4. **开发工程师 (Development Engineer)**
   - 执行具体的文件创建、修改任务
   - 使用工具完成文件操作和命令执行
   - 提交代码给审查员审查

5. **文档编写员 (Documentation Writer)**
   - 根据项目需求编写项目文档
   - 确保文档内容清晰、准确
   - 使用工具进行文件操作

6. **代码审查员 (Code Reviewer)**
   - 审查开发工程师提交的代码
   - 确保代码符合质量标准和最佳实践
   - 提供改进建议

## 配置说明

### 添加新角色

在 `communication/avatar.lua` 中添加新的角色定义：

```lua
{
    name = "新角色名称",
    model = "deepseek-reasoner",
    system = "角色系统提示词",
    tools = {"tool1", "tool2"},
    target = {"可对话的角色列表"},
    reserve_history = true  -- 是否保留对话历史（保留，目前无作用）
}
```

### 添加新工具

在 `communication/models.lua` 的 `tools` 数组中添加新工具：

```lua
{
    name = "新工具名称",
    description = "工具描述",
    tool = {
        type = "function",
        ["function"] = {
            name = "函数名称",
            description = "函数描述",
            parameters = {
                type = "object",
                properties = {
                    -- 参数定义
                },
                required = {"参数列表"}
            }
        }
    },
    action = function(input)
        -- 工具执行逻辑
        return {success = true, content = "执行结果"}
    end
}
```

### 添加新AI模型

在 `communication/models.lua` 中添加新的模型配置：

```lua
models.新模型名称 = {
    name = "模型显示名称",
    base_url = "API基础URL",
    api_type = "openai",  -- 或其他API类型
    authentication = {
        method = "API Key",
        api_key = "your-api-key"
    },
    models = {"可用模型列表"},
    tools = {--[[工具定义]]}
}
```

## 项目结构

```
AI-Team/
├── main.lua                    # 程序入口
├── README.md                   # 项目文档
└── communication/              # 核心通信模块
    ├── api.lua                 # API接口封装
    ├── avatar.lua              # 角色定义
    ├── communication.lua       # 通信管理器
    └── models.lua              # 模型配置
```

## 开发指南

### 扩展系统功能

1. **添加新API支持**：
   - 在 `api.lua` 中添加新的API类型实现
   - 遵循现有的 `api.openai` 模式

2. **自定义通信流程**：
   - 修改 `models.lua` 中的 `api_type`
   - 调整角色间的通信逻辑

3. **增强工具能力**：
   - 在 `models.lua` 中添加新的工具定义
   - 实现工具的具体执行逻辑

### 调试与测试

系统提供了交互式调试功能，在执行关键操作（如文件写入、命令执行）前会请求用户确认：

```
Proceed?[(Y)es/(n)o/(a)bort/yesforall]
```

- **Y/y**：继续执行
- **N/n**：跳过当前操作
- **A/a**：中止程序
- **yesforall**：后续所有同类操作自动确认

## 注意事项

1. API成本：使用DeepSeek API会产生费用，请合理控制使用量
2. 文件安全：系统可以执行文件操作和Shell命令，请谨慎使用
3. 对话历史：部分角色会保留对话历史，可能影响上下文长度
4. 错误处理：系统包含基本的错误处理，但复杂场景可能需要手动干预

## 许可证

本项目采用MIT许可证。

## 联系方式

- 项目仓库：https://github.com/imitoy/AI-Team（目前为私有仓库）
- 问题反馈：请使用GitHub Issues
- 作者邮箱：root@imitoy.top

---

**提示**：首次使用时，请确保已正确配置API密钥，并了解相关API的使用条款和费用。