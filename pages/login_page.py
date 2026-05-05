from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        # A pontos aldomain és elérési út (pontosan így írd be!)
        self.url = "https://practice.expandtesting.com/login"
        
        # Modern lokátorok: a felirat (label) alapján azonosítunk (4. és 5. kérdés javítása)
        self.username_field = page.get_by_label("Username")
        self.password_field = page.get_by_label("Password")
        # A gombot a szerepe és a felirata alapján keressük
        self.login_button = page.get_by_role("button", name="Login")

    def navigate(self):
        # A megadott URL-re navigálunk
        self.page.goto(self.url)

    def login(self, username, password):
        # Az __init__-ben definiált mezőket használjuk
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()