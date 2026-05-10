class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.login_btn = page.locator("button[type='submit']")

    def navigate(self):
        """Megnyitja a bejelentkező oldalt"""
        # Ide azt az URL-t írd, amit tesztelni szeretnél
        self.page.goto("https://practicetestautomation.com")

    def login(self, user, pwd):
        """Végrehajtja a bejelentkezést lassított gépeléssel"""
        self.username.press_sequentially(user, delay=200)
        self.password.press_sequentially(pwd, delay=200)
        self.login_btn.click()