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

class OnionSiteNavButton(NavButton):
    def __init__(self):
        super().__init__("http://h452fxjm2mv44hqytxahde4kjgg5tlbgd2un4yiqcfk3s35c2w63uryd.onion", "Tor Onion Site", "fa fa-globe")

class BlogNavButton(NavButton):
    def __init__(self):
        super().__init__("https://blog.skwal.net", "My Blog (fr)", "fa fa-book")