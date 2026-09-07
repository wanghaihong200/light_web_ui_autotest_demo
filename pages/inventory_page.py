"""saucedemo 商品列表页。"""

from __future__ import annotations

from light_web_ui_tester.pom import BaseComponent, BasePage


class CartBadge(BaseComponent):
    """购物车角标组件(页头右上角)。"""

    def __init__(self, page) -> None:
        super().__init__(page, root_selector=".shopping_cart_link")

    def count_text(self) -> str:
        """角标数字文本;无商品时角标元素不存在,按 '0' 处理。"""
        return self.el(".shopping_cart_badge", "购物车角标").inner.text_content() or "0"


class InventoryPage(BasePage):
    """商品列表页:加购、查看角标。"""

    def add_item_by_name(self, item_name: str) -> None:
        """按商品名加入购物车。"""
        self.el(
            f".inventory_item:has-text('{item_name}') button[data-test^='add-to-cart']",
            f"加购按钮:{item_name}",
        ).click()
