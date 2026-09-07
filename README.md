# light-web-ui-autotest-demo

`light-web-ui-tester` wheel 的冒烟验证用例项目(框架仓库:`../light_web_ui_tester`)。

被测站点为 [saucedemo.com](https://www.saucedemo.com)(Sauce Labs 官方模拟电商),以「登录 → 商品列表 → 加购」购物主流程为载体,验证框架的登录态缓存、POM 分层、软断言三条核心链路。

## Demo 场景

| # | 链路 | 用例 | 场景与验证点 |
|---|------|------|--------------|
| 1 | 登录态缓存 | `test_01_account_login_state` | `@pytest.mark.account("standard")` 标注后直达受保护页 `/inventory.html`:首跑触发登录钩子完成登录并写 `.auth/dev-standard.json`,重跑由 context 注入 `storage_state` 免登录 |
| 2 | POM 分层 | `test_02_pom_flow` | 手动走登录页 → 加购 `Sauce Labs Backpack` → 断言购物车角标计数为 `1`:厚 `BasePage` / `BaseComponent` 分层 + 业务等待,全程 Playwright 自动等待、零 sleep |
| 3 | 软断言 + Allure | `test_03_soft_assert` | 商品列表页追加多条业务断言到 `soft.that`:失败被收集而非中断,fixture teardown 自动 `assert_all`,结果进 Allure 报告 |
| 4 | 账号隔离 | `test_file_bound_to_performance_login_state` | `pytestmark` 整文件绑定 performance 账号直达受保护页,借 saucedemo 的 `session-username` 会话 cookie 断言身份,证明登录态确实来自 `performance_glitch_user` 而非 standard |

**登录态轴是账号,不是文件**:单用例级 marker(`test_smoke.py`)与文件级 `pytestmark`(`test_performance_account.py`)各占一个账号,`.auth/` 下按账号生成独立缓存(`dev-standard.json` / `dev-performance.json`),互不串扰。

### 项目结构

```
light_web_ui_autotest_demo/
├── config/
│   └── dev.yaml                     # 框架配置:base_url + standard/performance 双账号 + 超时
├── pages/
│   ├── login_page.py                # LoginPage(BasePage):填写凭据并提交
│   └── inventory_page.py            # InventoryPage(BasePage) + CartBadge(BaseComponent):加购、角标
├── tests/
│   ├── test_smoke.py                # 三条核心链路各一用例
│   └── test_performance_account.py  # 文件级登录态 + 身份隔离断言
├── conftest.py                      # register_login_hook 登录钩子(框架要求的唯一必写项)
└── pyproject.toml
```

## 复现步骤

```bash
# 1. 构建框架 wheel(框架仓库)
cd ../light_web_ui_tester && uv build && cd ../light_web_ui_autotest_demo

# 2. 安装 wheel(依赖由 wheel 元数据自动拉取)
uv pip install ../light_web_ui_tester/dist/light_web_ui_tester-0.1.0-py3-none-any.whl

# 3. 浏览器(幂等)
uv run playwright install chromium

# 4. 冒烟(需外网:被测站点 saucedemo.com)
rm -rf .auth allure-results
uv run pytest --alluredir=allure-results -v --headed --slowmo 500 # 有头 + 放慢 500ms,便于观察动作
uv run pytest tests/test_smoke.py::test_02_pom_flow --headed   # 单用例有头调试
```

## 通过判定

1. `4 passed`;
2. `.auth/dev-standard.json` 与 `.auth/dev-performance.json` 生成(登录态按账号隔离缓存);
3. `allure-results/` 产出用例 json(查看:`allure serve allure-results`,allure CLI 需自行安装,依赖 Java)。

## 注意事项

- saucedemo 会话 cookie 约 600s 过期且框架无 TTL 失效判断:登录态复用用例(`@pytest.mark.account`)集体失败时,删 `.auth/` 冷启动重跑。
