# AGENTS.md

## 1. 项目概况 (Project Overview)
本应用是一个基于 **Dash + Feffery** 的全栈 Web 应用。
- **核心功能**: 获取 1688 数据（通过 Apify）、持久化存储至 PostgreSQL、在类 Excel 表格中展示、推送至 TikTok Shop。
- **目标**: 实现高效的数据流转与实时用户反馈。
### 1.1 需求明细
1. **Apify 采集模块**:
   - 输入: 1688 搜索参数 (offerIds/keywords).
   - 输出: 原始 JSON 数据，存入 `tk_fill_products` (基础数据) 和 `tk_fill_product_skus` (SKU 详情).
2. **数据处理模块**:
   - 触发: 手动触发同步逻辑。
   - 逻辑: 检查 `batch_id` 唯一性，处理数据清洗与格式化，更新至 PostgreSQL。
3. **前端展示模块**:
   - 组件: `AntdTable`。
   - 交互: 支持全选数据，点击“推送”按钮触发后台服务。
4. **TikTok 推送模块**:
   - 接口: 调用 TikTok 官方 API。
   - 文档：参考本地Doc接口说明或参考https://partner.tiktokshop.com/docv2/page/get-authorized-category-assets-202405接口文档；
   - 状态更新: 推送成功后，在表格中更新对应行的状态列，并弹出成功提示。


## 2. 角色分工 (Agent Roles)
在与 OpenCodeInterpreter 对话时，你可以指派以下角色：
- **@web_dev (前端开发)**: 负责 Dash 布局、Feffery 组件交互、UI 样式。
- **@data_engine (数据专家)**: 负责 SQLAlchemy 异步模型、数据库查询、数据清洗逻辑。
- **@api_handler (集成专家)**: 负责 Apify 与 TikTok Shop API 的对接、重试机制、错误处理。

## 3. 开发规范 (Development Standards)

### A. 前端交互 (UI & Interaction)
- **技术栈**: 严禁使用原生 `html` 或 `dcc` 组件，必须全部使用 `feffery_antd_components` (fac) 和 `feffery_utils_components` (fuc)。
- **表格规范**: 使用 `fac.AntdTable` 实现类 Excel 功能。使用 `rowSelectionType="checkbox"` + `rowSelectionWidth=50` 以支持批量推送。
- **自定义列渲染**: 使用 `renderOptions: {"renderType": "custom-format"}` 搭配 `customFormatFuncs` 实现列内容样式化。
- **实时反馈**: 必须使用 `fac.AntdMessage` 或 `fac.AntdNotification` 提供操作反馈。
- **布局**: 使用 `fac.AntdRow` 和 `fac.AntdCol` 进行栅格布局，严禁使用自定义 CSS 文件。
- **项目参考**: 开发中有任何问题可以参考Demo目录下的优秀案例，可以参考借鉴其中用到的开发技巧

### B. 后端逻辑 (Backend & DB)
- **异步处理**: 所有数据库与 API 调用必须使用 `async def` 和 `await`。
- **数据库**: 使用 `sqlalchemy.ext.asyncio` 和 `asyncpg`。
- **数据一致性**: 数据库写入必须包含重试逻辑；插入采用 `ON CONFLICT DO UPDATE` 实现幂等性。

### C. 代码风格 (Coding Style)
- **命名**: 变量和函数使用 `snake_case`，模块常量使用 `UPPER_CASE`。
- **类型提示**: 所有新函数必须添加 Python Type Hints (如 `list[str]`, `| None`)。
- **注释**: 代码关键逻辑需使用中文注释，说明意图。

## 4. 交互反馈规范 (Status & Feedback)
AI 在回答或执行任务时，请遵循以下状态标识：
- ✅ 成功 (Success)
- ❌ 失败 (Error)
- 🚀 推送中 (Pushing)
- 📊 数据加载中 (Loading)

## 5. 工作流建议 (Workflow)
- **修改规则**: 如果发现 AI 偏离了 Feffery 的使用习惯，请直接更新此文件。
- **任务拆分**: 对于复杂功能（如：数据推送），请要求 AI 分为：“设计模型 -> 编写 API 服务 -> 编写前端表格 -> 联调回调”。

## 6. 核心约束 (Core Constraints)
- **环境管理**: 必须在项目根目录使用 `uv` 管理虚拟环境。所有依赖必须更新并锁定在 `requirements.txt` 中。
- **沟通语言**: **始终使用中文**进行对话和解释。除非涉及代码变量命名或必须使用英文的技术关键词。
- **项目清晰度**: 所有复杂任务必须先拆解为逻辑模块，AI 在开始编码前应先通过"伪代码"或"模块规划"征求用户确认。

## 7. 开发日志规范 (Development Log)

### A. 记录原则
每遇到一个需要超过 5 分钟排查的问题，**必须记录到 `development_log.md`**，包含：
- **现象**：用户看到什么（报错信息、截图描述）
- **原因**：根因是什么
- **修复**：具体代码或配置修改

### B. 日志格式
```markdown
## N. 问题类别
### N.M 具体问题
**现象**：...
**原因**：...
**修复**：...
```

### C. AI 工作流
1. 遇到问题先查 `development_log.md` 是否有类似记录
2. 如果没有，排查并修复后**立即追加记录**
3. 写代码前检查日志中的"踩坑总结原则"，避免重复犯错
4. 修改 `AGENTS.md` 中的规范时，同步剔除过时内容（如已被废弃的 API 用法）

### D. 用户要求记录时
AI 应将当前会话中所有遇到的问题汇总，按类别整理到 `development_log.md`，包括上述三要素（现象、原因、修复）。
