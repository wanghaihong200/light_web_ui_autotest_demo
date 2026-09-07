"""saucedemo 登录页。"""

from __future__ import annotations

from light_web_ui_tester.pom import BasePage


class LoginPage(BasePage):
    """登录页:填写凭据并提交。"""

    def login(self, username: str, password: str) -> None:
        """填写凭据并点击登录,成功后跳转库存页。"""
        self.el("#user-name", "用户名输入框").fill(username)
        self.el("#password", "密码输入框").fill(password)
        self.el("#login-button", "登录按钮").click()
