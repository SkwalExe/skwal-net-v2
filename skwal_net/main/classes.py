class NavButton():
    def __init__(self, href, text, icon):
        self.href = href
        self.text = text
        self.icon = icon


class HomeNavButton(NavButton):
    def __init__(self):
        super().__init__("/", "Home", "fa fa-home")


class AccountNavButton(NavButton):
    def __init__(self):
        super().__init__("/profile", "Account", "fa fa-user")


class LoginNavButton(NavButton):
    def __init__(self):
        super().__init__("/login", "Login", "fa fa-sign-in-alt")
