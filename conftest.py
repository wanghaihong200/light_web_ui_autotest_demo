"""demo 用例项目侧配置:登录钩子是框架要求的唯一必写项。"""

from light_web_ui_tester.auth import register_login_hook

from pages.login_page import LoginPage


# saucedemo 会话 cookie 约 600s 过期,框架无 TTL 失效判断;缓存过旧删 .auth/ 重跑
@register_login_hook
def saucedemo_login(page, account):
    """storage_state 缓存缺失时,框架以临时 context 调用本钩子完成登录并缓存。

    注意:临时 context 只注入 base_url,不会自动导航,必须先 goto 登录页。
    """
    page.goto("/")
    LoginPage(page).login(account.username, account.password)
