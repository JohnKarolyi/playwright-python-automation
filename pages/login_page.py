class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_field = page.locator("#username")
        self.password_field = page.locator("#password")
        self.login_button = page.locator("#submit")

    def navigate(self):
        """
        Megnyitja a gyakorló bejelentkező oldalt.
        A 'domcontentloaded' paraméter megakadályozza a hálózati timeout (időtúllépés) hibákat, 
        mert nem várja meg a lassú külső scriptek vagy hirdetések betöltődését.
        """
        self.page.goto(
            "https://practicetestautomation.com/practice-test-login/", 
            wait_until="domcontentloaded"
        )

    def login(self, user, pwd):
        """Végrehajtja a bejelentkezést lassított gépeléssel"""
        self.username_field.press_sequentially(user, delay=100)
        self.password_field.press_sequentially(pwd, delay=100)
        self.login_button.click()