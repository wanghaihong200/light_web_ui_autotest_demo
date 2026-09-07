"""pytestmark 示例:整文件绑定一个账号,登录态与其他文件互不串扰。

pytestmark 是 pytest 的模块级 marker 约定:文件内所有用例自动带上该 marker,
无需逐个标注。本文件用例的 context 注入 .auth/dev-performance.json
(账号定义见 config/dev.yaml 的 performance 节)。
"""

import pytest

from light_web_ui_tester.pom import wait_for_url_contains

pytestmark = pytest.mark.account("performance")


def test_file_bound_to_performance_login_state(page):
    """整文件 marker 生效:直达受保护页,context 携带 performance 账号的会话。

    saucedemo 登录后会设置名为 session-username 的会话 cookie,值为登录名,
    借此断言身份,证明登录态确实来自 performance 账号而非 standard。
    """
    page.goto("/inventory.html")
    wait_for_url_contains(page, "/inventory.html")

    cookies = {c["name"]: c["value"] for c in page.context.cookies()}
    assert "session-username" in cookies, f"未找到会话 cookie,实际: {sorted(cookies)}"
    assert cookies["session-username"] == "performance_glitch_user", (
        f"期望 performance 身份,实际 {cookies['session-username']!r}"
    )
