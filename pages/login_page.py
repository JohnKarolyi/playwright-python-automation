from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://practice.expandtesting.com/login"
        self.username_field = page.locator("#username")

    def navigate(self):
        self.page.goto(self.url, wait_until="load")

    def fill_username_custom(self, email: str):
        # Itt van a te speciális logikád elrejtve
        self.username_field.wait_for(state="attached", timeout=10000)
        self.username_field.evaluate(f"(el) => el.value = '{email}'")
        self.username_field.focus()
        self.page.keyboard.press("Tab")

    def login(self, username, password):
        self.page.fill("#username", username)
        self.page.fill("#password", password)
        self.page.click("button[type='submit']")


    def verify_username(self, expected_email: str):
        expect(self.username_field).to_have_value(str(expected_email))