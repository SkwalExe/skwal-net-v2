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

# I will need to add more types like info, success, warning...
allowed_header_types = [
    "", 
    "error", 
    "error-bg"
]

class HeaderTitle():
    def __init__(self, title, **kwargs):        
        self.title = title
        self.center = "center" if kwargs.get("center", True) else ""
        self.type = kwargs.get("type", "")
        if not self.type in allowed_header_types:
            raise Exception(f"Invalid header type: {self.type}")

    def render(self):
        return f"<h1 class='{self.center} {self.type}'>{self.title}</h1>"

    def __str__(self):
        return self.render()
    

class HeaderContent():
    def __init__(self, content):
        self.content = content

    def render(self):
        return f"<p>{self.content}</p>"

    def __str__(self):
        return self.render()

class Header():
    def __init__(self, title, content=None):
        
        self.title = title.render() if title is HeaderTitle else  HeaderTitle(title).render()
        
        if content is None:
            self.content = ""
        else:
            self.content = content.render() if content is HeaderContent else HeaderContent(content).render()
    
    def render(self):
        return f"<div class='box flex column gap'>{self.title}{self.content}</div>"

    def __str__(self):
        return self.render()