class LoginPage:
    def __init__(self, page):
        self.page = page
        self._username = page.locator("#username")
        self._password = page.locator("#password")
        self._login_btn = page.locator("button[type='submit']")

    def login(self, user, pwd):
        # delay=200: 0.2 másodpercet vár minden leütött billentyű között
        self._username.press_sequentially(user, delay=200)
        self._password.press_sequentially(pwd, delay=200)
        self._login_btn.click()