"""wheel 冒烟:登录态复用 / BasePage POM / 软断言 + Allure 三条核心链路。"""

import pytest

from light_web_ui_tester.pom import wait_for_url_contains, wait_visible

from pages.inventory_page import CartBadge, InventoryPage
from pages.login_page import LoginPage


@pytest.mark.account("standard")
def test_01_account_login_state(page):
    """链路 1:配置加载 + 登录态缓存。首跑触发钩子登录并写 .auth 缓存,context 注入 storage_state 直达受保护页。"""
    page.goto("/inventory.html")
    wait_for_url_contains(page, "/inventory.html")
    assert "Products" in page.content()


def test_02_pom_flow(page):
    """链路 2:厚 BasePage + 业务等待。手动走登录页 → 加购 → 角标计数(全程 Playwright 自动等待,禁 sleep)。"""
    login = LoginPage(page)
    login.open("/")
    login.login("standard_user", "secret_sauce")

    wait_for_url_contains(page, "/inventory.html")
    inventory = InventoryPage(page)
    inventory.add_item_by_name("Sauce Labs Backpack")

    badge = CartBadge(page)
    wait_visible(badge.el(".shopping_cart_badge", "购物车角标").inner)
    assert badge.count_text() == "1", f"角标期望 1,实际 {badge.count_text()!r}"


@pytest.mark.account("standard")
def test_03_soft_assert(page, soft):
    """链路 3:软断言收集 + fixture teardown 自动 assert_all(恒真断言,冒烟保持全绿)。"""
    page.goto("/inventory.html")
    wait_for_url_contains(page, "/inventory.html")
    inventory = InventoryPage(page)

    # 业务软断言:追加新断言时保持恒真(失败路径由框架单测覆盖)
    soft.that("商品列表展示 6 个商品", lambda: assert_true(
        inventory.page.locator(".inventory_item").count() == 6,
        f"期望 6 个商品,实际 {inventory.page.locator('.inventory_item').count()}",
    ))
    soft.that("页面标题为 Products", lambda: assert_true(
        "Products" in page.content(), "页面应包含 Products 标题"
    ))


def assert_true(condition: bool, message: str) -> None:
    """软断言辅助:plain assert,经 soft.that 的 lambda 包裹后失败会被收集而非中断。"""
    assert condition, message
