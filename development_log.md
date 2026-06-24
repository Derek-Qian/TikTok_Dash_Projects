# 开发日志

> 项目：TikTok 1688 商品同步管理（Dash + Feffery）
> 记录所有踩过的坑，避免再犯

---

## 1. 数据库连接

### 1.1 密码特殊字符导致 URL 解析错误
**现象**：`DATABASE_URL` 中密码含 `@` 和 `#`，URL 解析失败。

**原因**：`@` 被 URL 解析器当作 `user@host` 分隔符；`#` 被当作 URL fragment 标识（后面的内容被截断）。

**修复**：
```python
# config.py — 对密码做 URL 编码
from urllib.parse import quote
db_dsn = f"postgresql+asyncpg://{user}:{quote(password, safe='')}@{host}:{port}/{db}"
```
```ini
# .env — 密码加双引号，防止 dotenv 把 # 当注释符
DB_PASSWORD="Sxjsmf2023_!@#"
```

### 1.2 DNS 域名间歇性不可解析
**原因**：`www.sxjsmf.work` 域名偶尔解析失败。

**修复**：`.env` 中 `DB_HOST` 直接用 IP 地址 `129.211.210.245`，避免依赖 DNS。

### 1.3 Config 模块缓存导致 .env 修改不生效
**现象**：修改 `.env` 后程序仍读旧值。

**原因**：
- `load_dotenv()` 默认 `override=False`，不覆盖已存在的环境变量
- `__pycache__/*.pyc` 缓存旧字节码，Python 不重新执行模块

**修复**：
```python
# config.py
load_dotenv(override=True)  # 强制覆盖已有环境变量
```
```bash
# 每次 .env 变更后清理缓存
find . -path ./.venv -prune -o -name '__pycache__' -type d -exec rm -rf {} +
```

---

## 2. 异步数据库（SQLAlchemy + asyncpg）

### 2.1 全局 async engine 导致连接池竞争
**现象**：
```
asyncpg.exceptions.InterfaceError: cannot perform operation: another operation is in progress
```

**原因**：Web 回调中多次 `asyncio.run()` 共享同一个全局 `async_engine`，不同事件循环间连接池状态污染。

**修复**：**禁止全局共享 engine**。每次回调调用独立创建 engine + 用完 dispose：

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def create_session():
    engine = None
    try:
        engine = create_async_engine(config.db_dsn, pool_size=2, max_overflow=5)
        factory = async_sessionmaker(bind=engine, class_=AsyncSession)
        async with factory() as session:
            yield session
    finally:
        if engine is not None:
            await engine.dispose()
```

**原则**：在 `asyncio.run()` 场景下，每个调用拥有独立的引擎和连接池。

---

## 3. Dash + feffery 组件 API 差异

### 3.1 AntdTable 参数名
feffery v0.4.6 与标准 Ant Design / 文档的差异：

| 期望的写法 | feffery 实际 API |
|---|---|
| `rowSelection=True` | `rowSelectionType="checkbox"` + `rowSelectionWidth=50` |
| `editable=True`（顶层） | 仅每列 `columns[i].editable` 控制 |
| `rowSelectionType="radio"` | 单选模式 |

### 3.2 组件名称
- `FefferyExecute` → `FefferyExecuteJs`
- `app.run_server()` → `app.run()`（Dash 新版本）

### 3.3 AntdMessage 显示方式
**错误做法**：放在 `FefferyExecuteJs` 里 → 不显示
**正确做法**：放在普通容器中作为 children
```python
# 布局中
fac.AntdCenter(id="global-message")

# 回调中返回
return fac.AntdMessage(type="success", content="同步完成")
```

### 3.4 FefferyTimeout 事件属性
**错误**：`Input("xxx", "nClicks")`
**正确**：`Input("xxx", "timeoutCount")`
```python
fuc.FefferyTimeout(id="table-init-trigger", delay=100)  # 100ms 后触发
```

---

## 4. Dash 回调机制

### 4.1 allow_duplicate 必须搭配 prevent_initial_call
**现象**：
```
DuplicateCallback: allow_duplicate requires prevent_initial_call to be True
```

**规则**：当多个回调输出到同一组件属性时，所有回调都必须：
```python
Output("component-id", "prop", allow_duplicate=True)
# 必须同时
prevent_initial_call=True
```

### 4.2 回调模块必须显式导入才会注册
**错误**：写了回调文件但从不 import，回调不生效
**正确**：在 `app.py` 中显式导入（即使是 side-effect only）
```python
import src.web.callbacks.sync_callbacks  # noqa: F401, E402
import src.web.callbacks.table_callbacks  # noqa: F401, E402
import src.web.callbacks.detail_callbacks  # noqa: F401, E402
```

### 4.3 阻塞回调中 spinner 的显示
**问题**：同步回调阻塞线程，spinner 状态无法传回客户端。

**解决方案**：利用 Dash 乐观更新 + 独立回调
```python
# 回调 A：处理业务（阻塞）
@callback(Output("btn-sync", "loading"), ...)
def handle_sync(n_clicks):
    # ... 阻塞操作 ...
    return False  # 最后关 loading

# 回调 B：利用 Dash 乐观 loading 状态控制 spinner
@callback(Output("sync-spinner", "spinning"), Input("btn-sync", "loading"))
def toggle_spinner(loading):
    return loading  # 按钮 loading=True 时 spinner 也转
```

**原理**：Dash 对 `loading` 属性做乐观更新（点击瞬间就变 True），回调 B 立即响应显示 spinner。

### 4.4 内置 loading vs AntdSpin 的区别
- `btn-sync.loading`：按钮自带的 loading 效果（虚线转圈），Dash 乐观更新
- `AntdSpin.spinning` + `FefferyExtraSpinner`：可自定义样式的遮罩层 spinner（如 push、metro 风格）

---

## 5. feffery 组件属性类型陷阱

### 5.1 recentlyCellClickColumn 返回字符串
**错误**：标注为 `dict[str, object]`，然后用 `.get("dataIndex")`
**实际**：返回的是字符串如 `"product_title"`，直接用 `==` 比较

### 5.2 AntdTable 的 renderOptions
| renderType | 效果 |
|---|---|
| `"mini-area"` | 迷你折线图 |
| `"mini-bar"` | 迷你柱状图 |
| `"custom-format"` | 搭配 `customFormatFuncs` 自定义渲染 |
| `"link"` | ❌ 不存在，会导致列不显示 |

### 5.3 自定义单元格样式
**正确做法**（`customFormatFuncs` + `React.createElement`）：
```python
columns=[
    {"dataIndex": "title", "renderOptions": {"renderType": "custom-format"}},
]
customFormatFuncs={
    "title": "(value) => React.createElement('span', {style: {color:'#1677ff', textDecoration:'underline', cursor:'pointer'}}, value)",
}
```

---

## 6. 项目运行环境

### 6.1 Python 路径问题
直接运行 `.py` 文件可能找不到 `src` 模块，统一用 `-m` 形式：
```bash
# ✅ 正确
uv run python -m src.web.app

# ❌ 可能失败
uv run python src/web/app.py
```

### 6.2 后台进程管理
Dash debug 模式会 fork 子进程，kill 时需要确保全部清理：
```bash
pkill -f "src.web.app"
```

---

## 7. 踩坑总结原则

1. **先看源码再写代码**：feffery 版本不同 API 差异大，遇到组件属性问题直接看 `.venv/lib/.../组件名.py` 中的 `available_properties`
2. **异步 + 同步桥接要隔离引擎**：`asyncio.run()` 场景下不要共享全局 async engine
3. **回调先 import 再调**：Dash 回调文件必须被导入才能注册
4. **allow_duplicate → prevent_initial_call**：这是硬性规则
5. **乐观 loading 做 loading 效果**：阻塞回调中，让独立回调监听 loading 属性来控制 UI
6. **组件属性类型要验证**：State 的 type hint 错误会在运行时暴露，先查一下返回什么类型
7. **TikTok 认证信息必须从 DB 读取，不可依赖 .env**：`app_key`、`app_secret`、`access_token`、`shop_cipher` 全部来自数据库表（`tk_auth_info` + `tk_shops`），代码中不得直接引用 `config.TIKTOK_*`

---

## 8. TikTok 推送相关

### 8.1 rowKey 不是 feffery AntdTable 的合法属性
**现象**：`TypeError: unexpected keyword argument: 'rowKey'`
**原因**：feffery v0.4.6 的 AntdTable 不支持 `rowKey` 参数
**修复**：用 `selectedRows` 代替 `selectedRowKeys`，从完整行数据中取 `product_id`
```python
State("data-table", "selectedRows")  # ✅ 返回完整行数据列表
```

### ### 8.3 Debug 模式下 reloader 导致 DB 连接频繁 reset
**现象**：`ConnectionResetError: [Errno 104] Connection reset by peer`，`asyncio.run()` 中每次 `create_session()` 都连接失败
**原因**：Dash `debug=True` 会 fork reloader 进程，导致多个事件循环共享连接池状态或 DB server 拒绝过多连接
**修复**：非 debug 模式下运行 (`app.run(debug=False)`) 或使用持久化 engine 单例 (`pool_pre_ping=True`)

---

8.2 凭证必须从 DB 获取
**现象**：`Invalid 'app_key' query parameter`（用 .env 里的值不对）
**原因**：TikTok 认证凭证全部存于数据库表，不应从 `.env` 读取
**涉及的表**：
- `tk_auth_info` → `app_key`, `app_secret`, `access_token`
- `tk_shops` → `shop_cipher`（通过 `app_key` 关联）
**修复**：使用 JOIN 查询一次性获取全部凭证，`TikTokApiClient` 构造函数接收显式参数

### 8.4 推送失败：Product package size is invalid
**现象**：TikTok 返回 `code=12052116`：`Product package size is invalid. You cannot enter 0 or other non-numeric characters.`

**原因**：商品原始数据中只有 `unitWeight`（克），没有 `packageSize` / `packageDimensions`。`transform_1688_to_tiktok` 只传了 `package_weight`，没传 `package_dimensions`，TikTok 校验失败。

**修复**：
- `transformer.py`：当存在重量但缺失尺寸时，自动补充默认小包装尺寸 `10x10x10 cm`
- 修正 `unitWeight` 转换：统一按克转千克（除以 1000），不再只在 `>1` 时转换

### 8.5 推送失败：The warehouse does not exist
**现象**：TikTok 返回 `code=12052097`：`The warehouse does not exist. Nonexistent warehouse ID(s): 0`

**原因**：`tk_warehouses` 表中缓存的仓库 ID 已失效（TikTok 接口返回的仓库 ID 与历史数据不一致），`get_default_warehouse_id` 选到了不存在的旧 ID。

**修复**：
- `repository.py`：`upsert_warehouses` 在同步时清理不在新列表中的旧仓库记录
- `repository.py`：`get_default_warehouse_id` 优先选择 `is_default = TRUE` 的仓库，其次选择 `type = 'SALES_WAREHOUSE'` 的仓库，避免误选 RETURN 仓库

### 8.6 仓库同步时 datetime timezone 错误
**现象**：调用 `upsert_warehouses` 报错：`can't subtract offset-naive and offset-aware datetimes`

**原因**：`tk_warehouses.created_at` 字段是 `DateTime(timezone=False)`（无时区），但 `upsert_warehouses` 使用了 `datetime.now(timezone.utc)`（带时区）。

**修复**：`repository.py` 中 `upsert_warehouses` 使用与表定义一致的本地时间 `_now()`（无时区）。
